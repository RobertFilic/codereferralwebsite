from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS codes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  code TEXT UNIQUE NOT NULL,
                  service_id INTEGER NOT NULL,
                  created_at TIMESTAMP NOT NULL,
                  valid_until TIMESTAMP NOT NULL,
                  description TEXT,
                  is_valid BOOLEAN NOT NULL DEFAULT 1,
                  FOREIGN KEY (service_id) REFERENCES services (id))''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')


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

    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO codes (code, service_id, created_at, valid_until, description) VALUES (?, ?, ?, ?, ?)",
                  (code, service_id, created_at, valid_until, description))
        conn.commit()
        return jsonify({"message": "Code submitted successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Code already exists"}), 400
    finally:
        conn.close()


@app.route('/retrieve', methods=['GET'])
def retrieve_code():
    service_id = request.args.get('service_id')
    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
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

    c.execute(query, params)
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({
            "id": result[0],
            "code": result[1],
            "service": result[2],
            "valid_until": result[3],
            "description": result[4]
        }), 200
    else:
        return jsonify({"error": "No valid codes available"}), 404


@app.route('/codes', methods=['GET'])
def get_codes():
    service_id = request.args.get('service_id')
    print("service_id= ", service_id)
    is_valid = request.args.get('is_valid')
    print("******************is_valid****************************")
    print("is_valis = ", is_valid)

    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()

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

    if is_valid is not None and is_valid.strip() != '':
        try:
            is_valid_int = int(is_valid)
            query += " AND c.is_valid = ?"
            params.append(is_valid_int)
        except ValueError:
            return jsonify({"error": "Invalid value for 'is_valid'. It must be an integer."}), 400
    else:
        # No filter on is_valid, return all codes
        pass


    c.execute(query, params)
    codes = c.fetchall()
    conn.close()

    return jsonify([{
        "id": code[0],
        "code": code[1],
        "service": code[2],
        "created_at": code[3],
        "valid_until": code[4],
        "description": code[5],
        "is_valid": bool(code[6])
    } for code in codes])


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    code_id = data.get('id')
    is_valid = data.get('is_valid')

    if code_id is None or is_valid is None:
        return jsonify({"error": "Code ID and validity status are required"}), 400

    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE codes SET is_valid = ? WHERE id = ?", (is_valid, code_id))
        conn.commit()
        return jsonify({"message": "Feedback submitted successfully"}), 200
    finally:
        conn.close()


@app.route('/view_codes')
def view_codes():
    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM codes")
    codes = c.fetchall()
    conn.close()
    return render_template('view_codes.html', codes=codes)

@app.route('/add_code')
def add_code():
    return render_template('add_code.html')

@app.route('/retrieve_code')
def retrieve_code_page():
    return render_template('retrieve_code.html')


@app.route('/services', methods=['GET'])
def get_services():
    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM services")
    services = [{"id": row[0], "name": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(services)


@app.route('/add_service', methods=['POST'])
def add_service():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Service name is required"}), 400

    conn = sqlite3.connect('referral_codes.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO services (name) VALUES (?)", (name,))
        conn.commit()
        return jsonify({"message": "Service added successfully", "id": c.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Service already exists"}), 400
    finally:
        conn.close()


@app.route('/manage_services')
def manage_services():
    return render_template('manage_services.html')


if __name__ == '__main__':
    app.run(debug=True)