from app import app
from flask import request, jsonify
from app.db import DatabaseManager
import sqlite3

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    code_id = data.get('id')
    is_valid = data.get('is_valid')

    if code_id is None or is_valid is None:
        return jsonify({"error": "Code ID and validity status are required"}), 400

    db = DatabaseManager()
    try:
        db.execute_query("UPDATE codes SET is_valid = ? WHERE id = ?", (is_valid, code_id))
        return jsonify({"message": "Feedback submitted successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500