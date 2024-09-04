import sqlite3
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from MatchBundler import MatchBundler
from User import User
import pandas as pd
from database import init_db
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a random secret key for security
app.permanent_session_lifetime = timedelta(days=1)
CORS(app, supports_credentials=True)

# Load match data and initialize match bundler
df = pd.read_csv('Data/lol_match_data.csv')
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]
match_bundler = MatchBundler(df, features)

# Initialize the database
init_db()


# Registration route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Input Validation
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 40

    user = User(username, password)

    try:
        user.save_to_db()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred: ' + str(e)}), 500


# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    #Create User Instance
    user = User(username, password)

    #Load Guessing Data
    user.load_from_db()

    if user.verify_password(password):
        session['username'] = username
        session.permanent = True
        #print(f"Session set for user: {session['username']}")  # Debug statement
        return jsonify({'message': 'Login successful', 'stats': user.get_stats()})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Logout route
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})


# Get match data
@app.route('/api/match', methods=['GET'])
def get_match():

    # Retrieve username from session
    username = session['username']
    #print(f"Retrieved session username: {username}")  # Debug statement

    # Create a User object using the username
    user = User(username, '')  # You can pass an empty string for the password here

    # Load user data from the database
    user.load_from_db()

    # Get the next match bundle
    match = match_bundler.get_next_bundle()
    print(match)

    # Ensure the match hasn't been seen by the user
    while match is not None and user.has_seen_match(match['match_matchId'].iloc[0]):
        match = match_bundler.get_next_bundle()

    if match is None:
        match_bundler.reset()
        return jsonify({'message': 'No more new matches available'}), 404

    match_id = match['match_matchId'].iloc[0]
    user.mark_match_seen(match_id)
    user.save_to_db()

    match_data = match.to_dict(orient='records')
    return jsonify(match_data)



# Get leaderboard
@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, correct_counter, incorrect_counter FROM users ORDER BY correct_counter DESC')
    rows = cursor.fetchall()
    conn.close()

    leaderboard = []
    for row in rows:
        total = row[1] + row[2]
        percentage = (row[1] / total) * 100 if total > 0 else 0
        leaderboard.append({
            'username': row[0],
            'correct': row[1],
            'percentage': f"{percentage:.2f}"
        })

    return jsonify(leaderboard)


if __name__ == '__main__':
    app.run(debug=True)
