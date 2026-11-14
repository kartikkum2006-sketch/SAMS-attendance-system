import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attendance import AttendanceManager


class TestAttendance(unittest.TestCase):
    def setUp(self):
        self.m = AttendanceManager()
        self.m.add_student("101", "Aman")
        self.m.add_course("CIC-309", "Software Engineering")

    def test_percentage_calculation(self):
        for d, p in [("2026-11-01", 1), ("2026-11-02", 1), ("2026-11-03", 0), ("2026-11-04", 1)]:
            self.m.mark("101", "CIC-309", p, d)
        self.assertEqual(self.m.percentage("101", "CIC-309"), 75.0)

    def test_no_records_gives_zero(self):
        self.assertEqual(self.m.percentage("101", "CIC-309"), 0.0)

    def test_shortage_flag(self):
        self.m.mark("101", "CIC-309", 0, "2026-11-01")
        self.assertEqual(self.m.report("CIC-309")[0][3], "SHORTAGE")

    def test_duplicate_mark_overwrites(self):
        self.m.mark("101", "CIC-309", 0, "2026-11-01")
        self.m.mark("101", "CIC-309", 1, "2026-11-01")
        self.assertEqual(self.m.percentage("101", "CIC-309"), 100.0)

    def test_invalid_student_rejected(self):
        with self.assertRaises(ValueError):
            self.m.add_student("", "X")

    def test_unknown_student_rejected(self):
        with self.assertRaises(Exception):
            self.m.mark("999", "CIC-309", 1, "2026-11-01")


if __name__ == "__main__":
    unittest.main()
