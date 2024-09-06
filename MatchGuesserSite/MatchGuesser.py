from flask import Flask, request
from flask_cors import CORS
from api import api
from web import web
from database.db import db
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a random secret key for security
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MatchGuesser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web, url_prefix='/')

# Handle OPTIONS requests for CORS preflight
@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        # Allow specific headers and methods for preflight
        headers['Access-Control-Allow-Headers'] = 'Content-Type'
        headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'  # Replace with your frontend's origin
        headers['Access-Control-Allow-Credentials'] = 'true'

        return response


if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(rule)
    with app.app_context():  # Ensure app context is available for db.create_all()
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
