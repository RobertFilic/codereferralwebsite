from app import app
from flask import request, jsonify
from app.db import DatabaseManager
from datetime import datetime, timedelta
import sqlite3

@app.route('/submit', methods=['POST'])
def submit_code():
    data = request.json
    code = data.get('code')
    service_id = data.get('service_id')
    duration_days = int(data.get('duration', 30))
    description = data.get('description', '')

    if not code or not service_id:
        return jsonify({"error": "Code and service are required"}), 400

    created_at = datetime.now()
    valid_until = created_at + timedelta(days=duration_days)

    db = DatabaseManager()
    try:
        db.execute_query("INSERT INTO codes (code, service_id, created_at, valid_until, description) VALUES (?, ?, ?, ?, ?)",
                         (code, service_id, created_at, valid_until, description))
        return jsonify({"message": "Code submitted successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Code already exists"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500