from flask import Blueprint, jsonify, request, session


api = Blueprint('api', __name__)

@api.route('/rand_match', methods=['GET'])
def get_rand_match():
    match = fetch_match()

    if not match:
        return jsonify({"error": "No match found"}), 404

    # Convert match data to a list of dictionaries (one dictionary per player)
    match_data = [
        {
            'match_matchId': row[0],
            'player_teamId': row[1],
            'player_teamPosition': row[2],
            'player_lane': row[3],
            'player_champName': row[4],
            'player_banPickTurn': row[5],
            'player_champName_ban': row[6],
            'player_win': row[7],
        }
        for row in match
    ]

    return jsonify(match_data), 200
