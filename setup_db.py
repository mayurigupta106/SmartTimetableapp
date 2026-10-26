import sqlite3

conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

# Start fresh every time you run this file
cur.executescript("""
DROP TABLE IF EXISTS timetable_slots;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS sections;

CREATE TABLE sections (
    id INTEGER PRIMARY KEY, name TEXT, room TEXT);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY, code TEXT, name TEXT, is_lab INTEGER DEFAULT 0);

CREATE TABLE timetable_slots (
    id INTEGER PRIMARY KEY,
    section_id INTEGER, day INTEGER, period INTEGER,
    subject_id INTEGER, teacher_id INTEGER,
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id));
""")

# ---- Section ----
cur.execute("INSERT INTO sections (name, room) VALUES ('III CSIT-1', 'NLT-04')")
section_id = cur.lastrowid

# ---- Teachers (replace the last two with the real names) ----
teacher_names = {
    "MATHS": "Dr. Nitin",
    "UHVPE": "Dr. Upasana",
    "DS":    "Dr. Ruchi Gupta",
    "COA":   "Ms. Tanu Gupta",
    "DSTL":  "DSTL Faculty",
    "PP":    "PP Faculty",
}
teacher_id = {}
for key, name in teacher_names.items():
    cur.execute("INSERT INTO teachers (name, department) VALUES (?, 'CSIT')", (name,))
    teacher_id[key] = cur.lastrowid

# ---- Subjects ----
subject_list = [
    ("MATHS", "BAS-303", "Maths IV", 0),
    ("UHVPE", "BVE-301", "UHVPE", 0),
    ("DS",    "BCS-301", "Data Structure", 0),
    ("COA",   "BCS-302", "COA", 0),
    ("DSTL",  "BCS-303", "DSTL", 0),
    ("PP",    "BCC-302", "PP", 0),
    ("L1", "LAB1", "COA Lab 1A / WD Lab 1B", 1),
    ("L2", "LAB2", "Mini Project 1A / DS Lab 1B", 1),
    ("L3", "LAB3", "WD Lab 1A / COA Lab 1B", 1),
    ("L4", "LAB4", "DS Lab 1A / Mini Project 1B", 1),
]
subject_id = {}
for key, code, name, is_lab in subject_list:
    cur.execute("INSERT INTO subjects (code, name, is_lab) VALUES (?, ?, ?)",
                (code, name, is_lab))
    subject_id[key] = cur.lastrowid

# ---- Timetable: 9 periods per day, "-" means break ----
week = [
    "DS UHVPE UHVPE - COA MATHS - PP DSTL",       # Monday
    "L1 L1 DS - MATHS DSTL - MATHS UHVPE",        # Tuesday
    "MATHS DSTL DS - L2 L2 - COA PP",             # Wednesday
    "DSTL DS MATHS - L3 L3 - COA COA",            # Thursday
    "L4 L4 DSTL - COA DS - UHVPE MATHS",          # Friday
]
for day, line in enumerate(week):                 # day 0 = Monday
    for i, key in enumerate(line.split()):
        if key == "-":
            continue                              # skip breaks
        t_id = teacher_id.get(key)                # labs have no teacher -> None
        cur.execute(
            "INSERT INTO timetable_slots (section_id, day, period, subject_id, teacher_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (section_id, day, i + 1, subject_id[key], t_id))

conn.commit()
conn.close()
print("Database created!")