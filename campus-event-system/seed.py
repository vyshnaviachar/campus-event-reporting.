# seed.py - create DB and sample data
import sqlite3
from datetime import datetime
conn = sqlite3.connect('campus.db')
cur = conn.cursor()

with open('schema.sql','r') as f:
    cur.executescript(f.read())

# insert sample colleges
cur.execute("INSERT INTO colleges (name) VALUES (?)", ("Alpha College",))
cur.execute("INSERT INTO colleges (name) VALUES (?)", ("Beta Institute",))

# students
students = [
    ("Vaishnavi HP","vaishnavi@example.com",1),
    ("Rohit Kumar","rohit@example.com",1),
    ("Asha R","asha@example.com",2),
    ("Kumar S","kumar@example.com",2)
]
cur.executemany("INSERT INTO students (name,email,college_id) VALUES (?,?,?)", students)

# events
events = [
    ("Hackathon 1","Hackathon","2025-09-10",1,"active",datetime.utcnow().isoformat()),
    ("Workshop ML","Workshop","2025-09-12",1,"active",datetime.utcnow().isoformat()),
    ("Tech Talk","Seminar","2025-09-15",2,"active",datetime.utcnow().isoformat())
]
cur.executemany("INSERT INTO events (name,type,date,college_id,status,created_at) VALUES (?,?,?,?,?,?)", events)

# registrations (student_id, event_id)
regs = [
    (1,1, datetime.utcnow().isoformat()),
    (2,1, datetime.utcnow().isoformat()),
    (1,2, datetime.utcnow().isoformat()),
    (3,3, datetime.utcnow().isoformat())
]
cur.executemany("INSERT INTO registrations (student_id,event_id,reg_date) VALUES (?,?,?)", regs)

# mark attendance for some regs
cur.execute("INSERT INTO attendance (reg_id,status,marked_at) VALUES (?,?,?)", (1,"Present",datetime.utcnow().isoformat()))
cur.execute("INSERT INTO attendance (reg_id,status,marked_at) VALUES (?,?,?)", (2,"Absent",datetime.utcnow().isoformat()))
cur.execute("INSERT INTO attendance (reg_id,status,marked_at) VALUES (?,?,?)", (3,"Present",datetime.utcnow().isoformat()))

# feedback
cur.execute("INSERT INTO feedback (reg_id,rating,given_at) VALUES (?,?,?)", (1,5,datetime.utcnow().isoformat()))
cur.execute("INSERT INTO feedback (reg_id,rating,given_at) VALUES (?,?,?)", (3,4,datetime.utcnow().isoformat()))

conn.commit()
conn.close()
print('seeded campus.db')