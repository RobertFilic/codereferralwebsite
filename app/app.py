from flask import Flask, request, jsonify, render_template
from db import DatabaseManager
from routes.index import index
from routes.submit_code import submit_code
from routes.retrieve_code_page import retrieve_code
from routes.get_codes import get_codes
from routes.submit_feedback import submit_feedback
from routes.view_codes import view_codes
from routes.add_code import add_code
from routes.retrieve_code_page import retrieve_code_page
from routes.get_services import get_services
from routes.add_service import add_service
from routes.manage_services import manage_services

app = Flask(__name__)

app.route('/', methods=['GET'])(index)
app.route('/submit', methods=['POST'])(submit_code)
app.route('/retrieve', methods=['GET'])(retrieve_code)
app.route('/codes', methods=['GET'])(get_codes)
app.route('/feedback', methods=['POST'])(submit_feedback)
app.route('/view_codes')(view_codes)
app.route('/add_code')(add_code)
app.route('/retrieve_code')(retrieve_code_page)
app.route('/services', methods=['GET'])(get_services)
app.route('/add_service', methods=['POST'])(add_service)
app.route('/manage_services')(manage_services)

if __name__ == '__main__':
    app.run(debug=True)