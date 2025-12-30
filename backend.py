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

if __name__ == "__main__":
    create_tables()
    initialize_pet()
    print("Database and tables created successfully")
