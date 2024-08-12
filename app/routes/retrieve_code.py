from app import app
from flask import request, jsonify
from app.db import DatabaseManager
from datetime import datetime

@app.route('/retrieve', methods=['GET'])
def retrieve_code():
    service_id = request.args.get('service_id')
    db = DatabaseManager()
    now = datetime.now()

    query = """
    SELECT c.id, c.code, s.name, c.valid_until, c.description 
    FROM codes c
    JOIN services s ON c.service_id = s.id
    WHERE c.valid_until > ? AND c.is_valid = 1
    """
    params = [now]

    if service_id:
        query += " AND c.service_id = ?"
        params.append(service_id)

    query += " ORDER BY RANDOM() LIMIT 1"

    result = db.execute_query(query, params)

    if result:
        code = result[0]
        return jsonify({
            "id": code[0],
            "code": code[1],
            "service": code[2],
            "valid_until": code[3],
            "description": code[4]
        }), 200
    else:
        return jsonify({"error": "No valid codes available"}), 404