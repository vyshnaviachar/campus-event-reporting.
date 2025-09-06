# README - Campus Event Reporting System 

## What is included
- app.py — Flask app with APIs for events, registrations, attendance, feedback, and reports.
- schema.sql — Database schema for SQLite.
- seed.py — Script to create `campus.db` and insert sample data.
- queries.sql — Example reporting SQL queries.
- design_doc.md — Design document for the system.
- run.sh — Helper script to set up and run the project locally.

## How to set up (local machine)
1. Ensure Python 3.8+ is installed.
2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\\Scripts\\activate
3. Install requirements:
   pip install flask
4. Initialize DB with sample data:
   python seed.py
5. Run the app:
   python app.py
6. Use curl or Postman to call the endpoints. Example:
   curl -X GET http://127.0.0.1:5000/reports/event-popularity

## YOUR_PERSONAL_SECTION
Write here (in your own words):
- What you built and why.
- Key design choices and why you made them.
- How you tested the prototype.
- Any limitations and next steps you would implement.
- Attach screenshots of your AI conversation log (required by assignment).

## Notes for submission
- Replace this README with your personally written version before zipping and submitting.
- Make sure to include AI conversation screenshots separately as required by the assignment.
