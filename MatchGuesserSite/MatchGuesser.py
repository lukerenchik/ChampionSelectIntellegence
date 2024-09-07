from flask import Flask, request
from flask_cors import CORS
from api import api
from web import web
from database.db import init_db, db
import os
from sqlalchemy import text
from models.models import User



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a random secret key for security
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}}, supports_credentials=True)

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = f'sqlite:///{os.path.join(basedir, "database", "MatchGuesser.db")}'
print(f"Database URI: {db_uri}")  # Print the URI to verify it

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


with app.app_context():
    with app.app_context():
        User.add_user('test', 'testtest')
    try:
        # Open a session and execute a simple query to check the connection
        with db.session() as session:
            result = session.execute(text("SELECT 1")).fetchall()
            print("Database connection successful:", result)
    except Exception as e:
        print("Database connection failed:", str(e))

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
    app.run(debug=True)
