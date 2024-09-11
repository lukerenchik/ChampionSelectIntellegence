from flask import Blueprint, jsonify, request, session
from MatchGuesserSite.database.MatchFetcher import fetch_random_match


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
