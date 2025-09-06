from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

DB_PATH = "campus.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

# Create a helper to run queries
def query(sql, params=(), fetch=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    if fetch:
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    else:
        conn.commit()
        conn.close()
        return None

@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    required = ['name','type','date','college_id']
    for k in required:
        if k not in data:
            return jsonify({"error": f"missing {k}"}), 400
    sql = "INSERT INTO events (name, type, date, college_id, status, created_at) VALUES (?,?,?,?,?,?)"
    query(sql, (data['name'], data['type'], data['date'], data['college_id'], data.get('status','active'), datetime.utcnow().isoformat()))
    return jsonify({"message":"event created"}), 201

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    required = ['student_id','event_id']
    for k in required:
        if k not in data:
            return jsonify({"error": f"missing {k}"}), 400
    # prevent duplicate
    existing = query("SELECT * FROM registrations WHERE student_id=? AND event_id=?", (data['student_id'], data['event_id']), fetch=True)
    if existing:
        return jsonify({"error":"already registered"}), 400
    query("INSERT INTO registrations (student_id, event_id, reg_date) VALUES (?,?,?)", (data['student_id'], data['event_id'], datetime.utcnow().isoformat()))
    return jsonify({"message":"registered"}), 201

@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    required = ['reg_id','status']
    for k in required:
        if k not in data:
            return jsonify({"error": f"missing {k}"}), 400
    query("INSERT INTO attendance (reg_id, status, marked_at) VALUES (?,?,?)", (data['reg_id'], data['status'], datetime.utcnow().isoformat()))
    return jsonify({"message":"attendance marked"}), 201

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    required = ['reg_id','rating']
    for k in required:
        if k not in data:
            return jsonify({"error": f"missing {k}"}), 400
    rating = data['rating']
    if not (1 <= int(rating) <= 5):
        return jsonify({"error":"rating must be 1-5"}), 400
    query("INSERT INTO feedback (reg_id, rating, given_at) VALUES (?,?,?)", (data['reg_id'], rating, datetime.utcnow().isoformat()))
    return jsonify({"message":"feedback recorded"}), 201

# Reports
@app.route('/reports/event-popularity', methods=['GET'])
def event_popularity():
    sql = """
    SELECT e.event_id, e.name, e.type, e.college_id, COUNT(r.reg_id) as total_registrations
    FROM events e
    LEFT JOIN registrations r ON e.event_id = r.event_id
    WHERE e.status='active'
    GROUP BY e.event_id
    ORDER BY total_registrations DESC
    """
    rows = query(sql, fetch=True)
    return jsonify(rows), 200

@app.route('/reports/student-participation', methods=['GET'])
def student_participation():
    sql = """
    SELECT s.student_id, s.name, s.email, COUNT(a.att_id) as events_attended
    FROM students s
    LEFT JOIN registrations r ON s.student_id = r.student_id
    LEFT JOIN attendance a ON r.reg_id = a.reg_id AND a.status='Present'
    GROUP BY s.student_id
    ORDER BY events_attended DESC
    """
    rows = query(sql, fetch=True)
    return jsonify(rows), 200

@app.route('/reports/top-students', methods=['GET'])
def top_students():
    sql = """
    SELECT s.student_id, s.name, s.email, COUNT(a.att_id) as events_attended
    FROM students s
    LEFT JOIN registrations r ON s.student_id = r.student_id
    LEFT JOIN attendance a ON r.reg_id = a.reg_id AND a.status='Present'
    GROUP BY s.student_id
    ORDER BY events_attended DESC
    LIMIT 3
    """
    rows = query(sql, fetch=True)
    return jsonify(rows), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
