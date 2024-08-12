from app import app
from flask import render_template

@app.route('/manage_services')
def manage_services():
    return render_template('manage_services.html')