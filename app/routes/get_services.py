from app import app
from flask import jsonify
from app.db import DatabaseManager

@app.route('/services', methods=['GET'])
def get_services():
    db = DatabaseManager()
    services = db.execute_query("SELECT id, name FROM services")
    return jsonify([{"id": row[0], "name": row[1]} for row in services])