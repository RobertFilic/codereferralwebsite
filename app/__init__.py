from flask import Flask, jsonify
from app.logging_config import setup_logging


app = Flask(__name__)
setup_logging(app)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    return jsonify({"error": "An unexpected error occurred"}), 500

from app.routes.index import index
from app.routes.submit_code import submit_code
from app.routes.retrieve_code import retrieve_code
from app.routes.get_codes import get_codes
from app.routes.submit_feedback import submit_feedback
from app.routes.view_codes import view_codes
from app.routes.add_code import add_code
from app.routes.retrieve_code_page import retrieve_code_page
from app.routes.get_services import get_services
from app.routes.add_service import add_service
from app.routes.manage_services import manage_services