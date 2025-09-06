-- queries.sql: example reports
-- 1. Event Popularity (registrations per event)
SELECT e.event_id, e.name, COUNT(r.reg_id) AS total_registrations
FROM events e
LEFT JOIN registrations r ON e.event_id = r.event_id
WHERE e.status='active'
GROUP BY e.event_id
ORDER BY total_registrations DESC;

-- 2. Attendance Percentage per event
SELECT e.event_id, e.name,
  SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) as present_count,
  COUNT(r.reg_id) as total_registrations,
  ROUND( CAST(SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(r.reg_id) * 100, 2) as attendance_percentage
FROM events e
LEFT JOIN registrations r ON e.event_id = r.event_id
LEFT JOIN attendance a ON r.reg_id = a.reg_id
GROUP BY e.event_id;

-- 3. Average feedback score per event
SELECT e.event_id, e.name, AVG(f.rating) as avg_feedback
FROM events e
LEFT JOIN registrations r ON e.event_id = r.event_id
LEFT JOIN feedback f ON r.reg_id = f.reg_id
GROUP BY e.event_id;

-- 4. Top 3 most active students
SELECT s.student_id, s.name, COUNT(a.att_id) as events_attended
FROM students s
LEFT JOIN registrations r ON s.student_id = r.student_id
LEFT JOIN attendance a ON r.reg_id = a.reg_id AND a.status='Present'
GROUP BY s.student_id
ORDER BY events_attended DESC
LIMIT 3;