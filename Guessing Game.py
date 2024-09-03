from flask import Flask, jsonify
from flask_cors import CORS
from MatchBundler import MatchBundler
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load your match data into a DataFrame
df = pd.read_csv('Data/lol_match_data.csv')

# Define features and create an instance of MatchBundler (using your class)
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]

match_bundler = MatchBundler(df, features)


@app.route('/api/match', methods=['GET'])
def get_match():
    # Get the next match data from the bundler
    match = match_bundler.get_next_bundle()

    # If no more matches, reset or handle as needed (e.g., loop back to start)
    if match is None:
        match_bundler.reset()
        match = match_bundler.get_next_bundle()

    # Convert match DataFrame to JSON
    match_data = match.to_dict(orient='records')
    return jsonify(match_data)


if __name__ == '__main__':
    app.run(debug=True)
