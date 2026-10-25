"""SQLite database functions for the Student Performance Analyzer."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"


def save_students(dataframe):
    """Replace the students table with the cleaned dataset."""
    with sqlite3.connect(DB_PATH) as connection:
        dataframe.to_sql("students", connection, if_exists="replace", index=False)
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_students_percentage "
            "ON students(percentage)"
        )


def get_top_students(limit=5):
    """Return the highest-performing students using an SQL query."""
    query = """
        SELECT student_id, name, percentage, attendance
        FROM students
        ORDER BY percentage DESC, name ASC
        LIMIT ?
    """
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(query, (limit,)).fetchall()


def get_subject_averages():
    """Calculate subject averages with SQL."""
    query = """
        SELECT
            ROUND(AVG(math_marks), 2),
            ROUND(AVG(science_marks), 2),
            ROUND(AVG(english_marks), 2)
        FROM students
    """
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(query).fetchone()


def get_low_attendance(threshold=75):
    """Return students whose attendance is below the given threshold."""
    query = """
        SELECT student_id, name, attendance
        FROM students
        WHERE attendance < ?
        ORDER BY attendance ASC
    """
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(query, (threshold,)).fetchall()
