import pandas as pd
import psycopg2
from db import get_db_connection  # Import the connection function from db.py


class MatchLoader:
    def __init__(self, data_filepath, features):
        """
        Initialize the MatchLoader with a dataset and features to extract.

        :param data_filepath: CSV filepath containing the match data.
        :param features: List of column names to extract as features.
        """
        self.data_filepath = data_filepath
        self.features = features
        self.matches_df = self._csv_to_dataframe()

    def _csv_to_dataframe(self):
        """
        Convert the CSV match data to a Pandas DataFrame if needed.
        :return: A Pandas DataFrame containing the feature data.
        """
        try:
            df = pd.read_csv(self.data_filepath)
            return df[self.features]
        except FileNotFoundError:
            print(f"File {self.data_filepath} not found.")
            return pd.DataFrame()

    def load_matches_to_db(self):
        """
        Add the matches to the 'matches' table within the MatchGuesser database.

        :return: A status message indicating whether the matches were successfully added to the database.
        """
        if self.matches_df.empty:
            return "No match data to load."

        # Get the database connection
        conn = get_db_connection()
        if conn is None:
            return "Failed to connect to the database."

        try:
            cursor = conn.cursor()

            # Prepare the SQL insert statement
            insert_query = """
                INSERT INTO matches (
                    match_matchId, player_teamId, player_teamPosition,
                    player_lane, player_champName, player_banPickTurn,
                    player_champName_ban, player_win
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;  -- Optional: prevents duplicate entries if match_matchId is unique
            """

            # Iterate over the DataFrame and insert data into the database
            for index, row in self.matches_df.iterrows():
                cursor.execute(insert_query, (
                    row['match_matchId'], row['player_teamId'], row['player_teamPosition'],
                    row['player_lane'], row['player_champName'], row['player_banPickTurn'],
                    row['player_champName_ban'], row['player_win']
                ))

            # Commit the transaction and close the connection
            conn.commit()
            cursor.close()
            conn.close()
            return f"Successfully added {len(self.matches_df)} matches to the database."

        except psycopg2.DatabaseError as e:
            return f"Database error: {e}"

        except Exception as e:
            return f"Error: {e}"


# Load match data and initialize match loader
data_filepath = '/home/lightbringer/Documents/Dev/ChampionSelectIntelligence/Data/lol_match_data.csv'
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]

match_loader = MatchLoader(data_filepath, features)
status_message = match_loader.load_matches_to_db()
print(status_message)
