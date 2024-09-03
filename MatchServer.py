from MatchBundler import MatchBundler
import pandas as pd

# Load the CSV data into a pandas DataFrame
csv_file_path = 'Data/lol_match_data.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Define the features you are interested in
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]

# Create an instance of MatchBundler
bundler = MatchBundler(df, features)


bundle = bundler.get_next_bundle()

i = 0

while i < 15:
     print(bundle)
     bundle = bundler.get_next_bundle()
     i += 1
        