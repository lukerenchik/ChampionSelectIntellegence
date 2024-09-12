from flask import Blueprint, jsonify, request, session
from MatchGuesserSite.database.MatchFetcher import fetch_random_match
from MatchGuesserSite.database.Register import register_user


api = Blueprint('api', __name__)

@api.route('/rand_match', methods=['GET'])
def get_rand_match():
    match = fetch_random_match()

    if not match:
        return jsonify({"error": "No match found"}), 404

    match_matchId = match[0]  # The first element is the match ID
    player_data_list = match[1]  # The second element is the list of players

    # Convert player data to a list of dictionaries
    match_data = [
        {
            'match_matchId': match_matchId,  # Use the match ID for all players
            'player_teamId': row[2],  # Adjusted index for team ID
            'player_teamPosition': row[3],
            'player_lane': row[4],
            'player_champName': row[5],
            'player_banPickTurn': row[6],
            'player_champName_ban': row[7],
            'player_win': row[8],
        }
        for row in player_data_list
    ]

    return jsonify(match_data), 200

@api.route('/register', methods=['POST'])
def register():
    """
    API route to register a new user.
    It extracts the user details from the request and calls the register_user function.
    """
    try:
        # Extract user details from the POST request
        data = request.json  # Ensure this is JSON
        name = data.get('name')
        password = data.get('pass')

        # Check if name or password is missing
        if not name or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Call the registration function
        registration_successful = register_user(name, password)

        if registration_successful:
            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"error": "Failed to register user"}), 500

    except Exception as e:
        # Log the error for debugging
        print(f"Error in registration API: {e}")
        return jsonify({"error": "An internal error occurred"}), 500


