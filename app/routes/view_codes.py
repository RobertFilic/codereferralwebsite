from app import app
from flask import render_template
from app.db import DatabaseManager

@app.route('/view_codes')
def view_codes():
    db = DatabaseManager()
    codes = db.execute_query("SELECT * FROM codes")
    return render_template('view_codes.html', codes=codes)