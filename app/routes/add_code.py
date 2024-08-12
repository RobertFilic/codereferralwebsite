from app import app
from flask import render_template

@app.route('/add_code')
def add_code():
    return render_template('add_code.html')