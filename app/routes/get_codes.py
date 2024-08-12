from app import app
from flask import request, jsonify
from app.db import DatabaseManager

@app.route('/codes', methods=['GET'])
def get_codes():
    service_id = request.args.get('service_id')
    is_valid = request.args.get('is_valid')

    db = DatabaseManager()

    query = """
    SELECT c.id, c.code, s.name, c.created_at, c.valid_until, c.description, c.is_valid
    FROM codes c
    JOIN services s ON c.service_id = s.id
    WHERE 1=1
    """
    params = []

    if service_id:
        query += " AND c.service_id = ?"
        params.append(service_id)

    if is_valid is not None and is_valid != 'all':
        try:
            query += " AND c.is_valid = ?"
            params.append(int(is_valid))
        except ValueError:
            return jsonify({"error": "Invalid value for 'is_valid'. It must be 'all' or an integer."}), 400

    codes = db.execute_query(query, params)

    return jsonify([{
        "id": code[0],
        "code": code[1],
        "service": code[2],
        "created_at": code[3],
        "valid_until": code[4],
        "description": code[5],
        "is_valid": bool(code[6])
    } for code in codes])