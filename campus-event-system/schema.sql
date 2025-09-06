-- schema.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS colleges (
    college_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    college_id INTEGER,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    date TEXT,
    college_id INTEGER,
    status TEXT DEFAULT 'active',
    created_at TEXT,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id)
);

CREATE TABLE IF NOT EXISTS registrations (
    reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    event_id INTEGER,
    reg_date TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    UNIQUE(student_id, event_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    att_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_id INTEGER,
    status TEXT, -- 'Present' or 'Absent'
    marked_at TEXT,
    FOREIGN KEY (reg_id) REFERENCES registrations(reg_id)
);

CREATE TABLE IF NOT EXISTS feedback (
    fb_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_id INTEGER,
    rating INTEGER CHECK (rating>=1 AND rating<=5),
    given_at TEXT,
    FOREIGN KEY (reg_id) REFERENCES registrations(reg_id)
);
