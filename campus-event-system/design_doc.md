# Design Document - Campus Event Reporting System

## Assumptions
- Single database with `college_id` to separate colleges.
- Students can register for multiple events, but only once per event (unique constraint).
- Attendance is recorded per registration (reg_id).
- Feedback is optional and an integer rating 1–5.
- Event `status` can be 'active' or 'cancelled'. Cancelled events are excluded from popularity reports.

## Data to Track
- Event creation metadata
- Student registrations
- Attendance markings (Present/Absent)
- Feedback ratings (1–5)

## Database Schema
Tables: `colleges`, `students`, `events`, `registrations`, `attendance`, `feedback`.
(See schema.sql for full DDL.)

## API Design (selected endpoints)
- `POST /events` — create event (name, type, date, college_id)
- `POST /register` — register (student_id, event_id)
- `POST /attendance` — mark attendance (reg_id, status)
- `POST /feedback` — submit feedback (reg_id, rating)
- `GET /reports/event-popularity` — registrations per event
- `GET /reports/student-participation` — events attended per student
- `GET /reports/top-students` — top 3 active students

## Workflows
1. Registration: Student submits registration → Insert into `registrations` with timestamp.
2. Attendance: Admin marks attendance by referencing `reg_id` → Insert into `attendance`.
3. Feedback: Student submits rating linked to their `reg_id` → Insert into `feedback`.
4. Reporting: Aggregation queries run over tables to produce dashboards and CSV export.

## Edge Cases & Handling
- Duplicate registration -> prevented by UNIQUE(student_id,event_id).
- Missing attendance -> counted as absent for events when calculating attendance percentage (depends on business rule).
- Cancelled event -> mark `status='cancelled'` and exclude from active reports.
- Deleted student/event -> use soft-delete (not implemented in prototype).

## Scale considerations
- For ~50 colleges × 500 students × 20 events: ~500k rows across tables (manageable in a single DB); consider partitioning or per-college schemas for higher scale.
- Event IDs are unique globally in this design. To keep per-college separation, prefix IDs or use UUIDs if merging datasets in future.
