"""Student Attendance Management System (SAMS) - core module."""
import sqlite3
from datetime import date

THRESHOLD = 75.0  # minimum attendance percentage


class AttendanceManager:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS student(
                roll_no TEXT PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS course(
                code TEXT PRIMARY KEY, title TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS attendance(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT NOT NULL REFERENCES student(roll_no),
                code TEXT NOT NULL REFERENCES course(code),
                day TEXT NOT NULL, present INTEGER NOT NULL,
                UNIQUE(roll_no, code, day));
        """)

    def add_student(self, roll_no, name):
        if not roll_no or not name:
            raise ValueError("roll_no and name are required")
        self.conn.execute("INSERT INTO student VALUES (?,?)", (roll_no, name))
        self.conn.commit()

    def add_course(self, code, title):
        self.conn.execute("INSERT INTO course VALUES (?,?)", (code, title))
        self.conn.commit()

    def mark(self, roll_no, code, present, day=None):
        day = day or date.today().isoformat()
        self.conn.execute(
            "INSERT OR REPLACE INTO attendance(roll_no,code,day,present) "
            "VALUES (?,?,?,?)", (roll_no, code, day, 1 if present else 0))
        self.conn.commit()

    def percentage(self, roll_no, code):
        total, attended = self.conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(present),0) FROM attendance "
            "WHERE roll_no=? AND code=?", (roll_no, code)).fetchone()
        return 0.0 if total == 0 else round(100.0 * attended / total, 1)

    def report(self, code):
        rows = self.conn.execute(
            "SELECT roll_no, name FROM student ORDER BY roll_no").fetchall()
        out = []
        for roll_no, name in rows:
            pct = self.percentage(roll_no, code)
            out.append((roll_no, name, pct,
                        "OK" if pct >= THRESHOLD else "SHORTAGE"))
        return out
