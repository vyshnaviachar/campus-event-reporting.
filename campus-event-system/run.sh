#!/bin/bash
# run.sh - helper to create DB and run the Flask app
python3 -m venv venv || true
. venv/bin/activate
pip install flask || true
python seed.py
echo "Starting Flask app on http://0.0.0.0:5000 ..."
python app.py
