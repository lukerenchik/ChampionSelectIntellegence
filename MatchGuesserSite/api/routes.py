import sqlite3
from flask import Blueprint, jsonify, request, session


api = Blueprint('api', __name__)


# Registration route
@api.route('/api/register', methods=['POST'])
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
@api.route('/api/login', methods=['POST'])
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
@api.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})


# Get match data
@api.route('/api/match', methods=['GET'])
def get_match():
    """
    Get a random match from the database
    :return: a dataframe that contains match data
    """



# Get leaderboard
@api.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    conn = sqlite3.connect('../../users.db')
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

@api.route('/api/correct_guess', methods=['POST'])
def correct_guess():

    data = request.json
    game_id = data.get('gameId')
    username = session['username']
    user = User(username)
    user.load_from_db()

    # Check if the user has already seen this game
    if user.has_seen_match(game_id):
        return jsonify({'message': 'Game already evaluated'}), 400

    # Increment correct guess counter and mark game as seen
    user.increment_correct()
    user.mark_match_seen(game_id)

    # Save changes to the database
    user.save_to_db()

    return jsonify({
        'message': 'Correct guess recorded',
        'correct': user.correct_counter,
        'incorrect': user.incorrect_counter
    }), 200


@api.route('/api/incorrect_guess', methods=['POST'])
def incorrect_guess():

    data = request.json
    game_id = data.get('gameId')
    username = session['username']
    user = User(username)
    user.load_from_db()

    # Check if the user has already seen this game
    if user.has_seen_match(game_id):
        return jsonify({'message': 'Game already evaluated'}), 400

    # Increment incorrect guess counter and mark game as seen
    user.increment_incorrect()
    user.mark_match_seen(game_id)

    # Save changes to the database
    user.save_to_db()

    return jsonify({
        'message': 'Incorrect guess recorded',
        'correct': user.correct_counter,
        'incorrect': user.incorrect_counter
    }), 200