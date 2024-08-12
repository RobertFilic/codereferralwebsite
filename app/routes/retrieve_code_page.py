from app import app
from flask import render_template

@app.route('/retrieve_code')
def retrieve_code_page():
    return render_template('retrieve_code.html')