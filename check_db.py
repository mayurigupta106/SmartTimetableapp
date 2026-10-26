import sqlite3
conn = sqlite3.connect("timetable.db")
rows = conn.execute("""
    SELECT ts.day, ts.period, s.name, t.name
    FROM timetable_slots ts
    JOIN subjects s ON ts.subject_id = s.id
    LEFT JOIN teachers t ON ts.teacher_id = t.id
    WHERE ts.day = 3
    ORDER BY ts.period
""").fetchall()
for r in rows:
    print(r)