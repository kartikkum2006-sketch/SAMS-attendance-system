from attendance import AttendanceManager

m = AttendanceManager()
for r, n in [("101", "Aman"), ("102", "Riya"), ("103", "Kartik"), ("104", "Neha")]:
    m.add_student(r, n)
m.add_course("CIC-309", "Software Engineering")
pattern = {"101": [1,1,1,1,1,1,0,1], "102": [1,0,1,0,0,1,0,1],
           "103": [1,1,1,0,1,1,1,1], "104": [0,1,0,0,1,0,1,0]}
for r, marks in pattern.items():
    for i, p in enumerate(marks, 1):
        m.mark(r, "CIC-309", p, f"2026-11-{i:02d}")
print("ATTENDANCE REPORT - CIC-309 (Software Engineering)")
print(f"{'Roll':<6}{'Name':<10}{'Attendance %':<14}Status")
print("-" * 40)
for r, n, pct, st in m.report("CIC-309"):
    print(f"{r:<6}{n:<10}{pct:<14}{st}")
