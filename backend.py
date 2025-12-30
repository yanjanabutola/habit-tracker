import sqlite3
from datetime import date

# Connect to database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        log_date TEXT,
        completed INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pet_health (
        id INTEGER PRIMARY KEY,
        health INTEGER
    )
    """)

    conn.commit()


def initialize_pet():
    cursor.execute("SELECT * FROM pet_health WHERE id = 1")
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO pet_health (id, health) VALUES (1, 100)"
        )
        conn.commit()


def update_pet_health(completed, total, streak):
    """
    completed: habits done today
    total: total habits today
    streak: continuous days completed
    """
    if total == 0:
        return

    completion_rate = completed / total

    cursor.execute("SELECT health FROM pet_health WHERE id = 1")
    health = cursor.fetchone()[0]

    # Logic
    if completion_rate == 1:
        health += 5
    elif completion_rate >= 0.5:
        health += 1
    else:
        health -= 5

    # Streak bonus
    if streak >= 5:
        health += 3

    # Clamp health between 0–100
    health = max(0, min(100, health))

    cursor.execute(
        "UPDATE pet_health SET health = ? WHERE id = 1",
        (health,)
    )
    conn.commit()

    return health


def add_habit(name, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO habits (name, category) VALUES (?, ?)",
        (name, category)
    )

    conn.commit()
    conn.close()

def get_all_habits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category FROM habits")
    habits = cursor.fetchall()

    conn.close()
    return habits


def get_habits_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name FROM habits WHERE category = ?",
        (category,)
    )
    habits = cursor.fetchall()

    conn.close()
    return habits

def update_habit(habit_id, new_name, new_category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE habits SET name = ?, category = ? WHERE id = ?",
        (new_name, new_category, habit_id)
    )

    conn.commit()
    conn.close()

def delete_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM habit_log WHERE habit_id = ?",
        (habit_id,)
    )

    cursor.execute(
        "DELETE FROM habits WHERE id = ?",
        (habit_id,)
    )

    conn.commit()
    conn.close()

def log_habit(habit_id, completed, log_date=None):
    """
    completed: 1 = done, 0 = not done
    log_date: YYYY-MM-DD (default = today)
    """
    if log_date is None:
        log_date = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    # Check if entry already exists for this habit + date
    cursor.execute("""
        SELECT id FROM habit_log
        WHERE habit_id = ? AND log_date = ?
    """, (habit_id, log_date))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE habit_log
            SET completed = ?
            WHERE habit_id = ? AND log_date = ?
        """, (completed, habit_id, log_date))
    else:
        cursor.execute("""
            INSERT INTO habit_log (habit_id, log_date, completed)
            VALUES (?, ?, ?)
        """, (habit_id, log_date, completed))

    conn.commit()
    conn.close()

def get_today_completion(log_date=None):
    if log_date is None:
        log_date = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM habit_log
        WHERE log_date = ? AND completed = 1
    """, (log_date,))
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM habits")
    total = cursor.fetchone()[0]

    conn.close()
    return completed, total

def calculate_streak():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM habits")
    total_habits = cursor.fetchone()[0]

    if total_habits == 0:
        conn.close()
        return 0

    streak = 0
    current_date = date.today()

    while True:
        cursor.execute("""
            SELECT COUNT(*) FROM habit_log
            WHERE log_date = ? AND completed = 1
        """, (current_date.isoformat(),))

        completed = cursor.fetchone()[0]

        if completed == total_habits:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    conn.close()
    return streak

def update_health_for_today():
    completed, total = get_today_completion()
    streak = calculate_streak()
    return update_pet_health(completed, total, streak)

def get_week_date_range(year, month, week_number):
    """
    week_number: 1 to 4
    """
    start_day = (week_number - 1) * 7 + 1
    start_date = date(year, month, start_day)
    end_date = start_date + timedelta(days=6)
    return start_date, end_date

def get_weekly_stats(year, month, week_number):
    start_date, end_date = get_week_date_range(year, month, week_number)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM habits")
    total_habits = cursor.fetchone()[0]

    if total_habits == 0:
        conn.close()
        return 0

    total_days = 0
    completed_days = 0

    current = start_date
    while current <= end_date:
        cursor.execute("""
            SELECT COUNT(*) FROM habit_log
            WHERE log_date = ? AND completed = 1
        """, (current.isoformat(),))
        completed = cursor.fetchone()[0]

        if completed == total_habits:
            completed_days += 1

        total_days += 1
        current += timedelta(days=1)

    conn.close()

    return round((completed_days / total_days) * 100, 2)

def get_monthly_stats(year, month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM habits")
    total_habits = cursor.fetchone()[0]

    if total_habits == 0:
        conn.close()
        return 0

    cursor.execute("""
        SELECT COUNT(DISTINCT log_date)
        FROM habit_log
        WHERE completed = 1
        AND strftime('%Y', log_date) = ?
        AND strftime('%m', log_date) = ?
    """, (str(year), f"{month:02d}"))

    completed_days = cursor.fetchone()[0]

    # Approx days in month (good enough for project)
    days_in_month = 28 if month == 2 else 30

    conn.close()

    return round((completed_days / days_in_month) * 100, 2)

if __name__ == "__main__":
    create_tables()
    initialize_pet()

    # optional quick test
    print("Backend ready")
