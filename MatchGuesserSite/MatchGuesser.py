from flask import Flask
from flask_cors import CORS
from api import api
from web import web
from database.db import init_db
from models.user import User
from MatchGuesserSite.models.MatchLoader import MatchLoader
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a random secret key for security
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MatchGuesser.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
