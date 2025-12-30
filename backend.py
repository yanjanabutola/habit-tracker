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

