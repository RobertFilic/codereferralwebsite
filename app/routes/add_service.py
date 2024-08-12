from app import app
from flask import request, jsonify
from app.db import DatabaseManager
import sqlite3

@app.route('/add_service', methods=['POST'])
def add_service():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Service name is required"}), 400

    db = DatabaseManager()
    try:
        db.execute_query("INSERT INTO services (name) VALUES (?)", (name,))
        new_id = db.execute_query("SELECT last_insert_rowid()")[0][0]
        return jsonify({"message": "Service added successfully", "id": new_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Service already exists"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500