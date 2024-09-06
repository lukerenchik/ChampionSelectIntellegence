from flask import Blueprint, jsonify, request, session
from MatchGuesserSite.models.user import User
from MatchGuesserSite.models.match import MatchData
from MatchGuesserSite.database import db

api = Blueprint('api', __name__)


@api.route('/get_winning_team', methods=['GET'])
def get_winning_team():
    """
    Get the winning team (red or blue) from a match.
    The client should provide a match_id as a query parameter.
    """
    match_id = request.args.get('match_id')
    match = MatchData.query.filter_by(match_matchId=match_id).first()

    if match:
        return jsonify({'match_id': match_id, 'winning_team': 'red' if match.player_win else 'blue'})
    else:
        return jsonify({'error': 'Match not found'}), 404

@api.route('/correct_guess', methods=['POST'])
def correct_guess():
    """
        Increment the user's correct guesses in the database.
        """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.increment_correct_answers()
            return jsonify({'message': 'Correct guess updated'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'User not logged in'}), 401

@api.route('/incorrect_guess', methods=['POST'])
def incorrect_guess():
    """
        Increment the user's incorrect guesses in the database.
        """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.increment_incorrect_answers()
            return jsonify({'message': 'Incorrect guess updated'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'User not logged in'}), 401

@api.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    """
        Display the top X users based on their correct/incorrect guess ratio.
        """
    top_users = User.query.order_by(
        db.desc(User.correct_answers / (User.correct_answers + User.incorrect_answers))
    ).limit(10).all()

    leaderboard = []
    for user in top_users:
        correct = user.correct_answers
        incorrect = user.incorrect_answers
        total = correct + incorrect
        percentage = (correct / total) * 100 if total > 0 else 0
        leaderboard.append({
            'user_id': user.user_id,
            'correct_answers': correct,
            'incorrect_answers': incorrect,
            'percentage': percentage
        })

    return jsonify({'leaderboard': leaderboard}), 200

@api.route('/rand_match', methods=['GET'])
def get_rand_match():
    """
    Get a random match from the database that the user hasn't seen.
    :return: a JSON object containing match data
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    match = MatchData.get_random_unseen_match(user_id=user_id)
    if match:
        # Add the match to the user's seen matches
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.add_match_to_seen(match.match_matchId)

        return jsonify({
            'match_matchId': match.match_matchId,
            'player_teamId': match.player_teamId,
            'player_teamPosition': match.player_teamPosition,
            'player_lane': match.player_lane,
            'player_champName': match.player_champName,
            'player_banPickTurn': match.player_banPickTurn,
            'player_champName_ban': match.player_champName_ban,
            'player_win': match.player_win
        }), 200
    else:
        return jsonify({'error': 'No unseen matches found'}), 404


@api.route('/logout', methods=['POST'])
def logout():
    """
       Logs the user out of their session.
       """
    session.clear()  # Clear the session data
    return jsonify({'message': 'Logged out successfully'}), 200

@api.route('/login', methods=['POST'])
def login():
    """
        Authenticates the user by verifying the username and password.
        If the login is successful, the user ID is stored in the session.
        """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(user_id=username).first()
    if user and user.check_password(password):
        # Save user info in session
        session['user_id'] = user.user_id
        session['username'] = username

        return jsonify({'message': 'Login successful', 'user': {'id': user.user_id, 'username': username}})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@api.route('/register', methods=['POST'])
def register():
    """
        Registers a new user with a username and password.
        """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    existing_user = User.query.filter_by(user_id=username).first()
    if existing_user:
        return jsonify({'message': 'Username already taken'}), 400

    # Register the new user
    user = User.register_user(password)
    user.user_id = username  # Assign the username to the user
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201