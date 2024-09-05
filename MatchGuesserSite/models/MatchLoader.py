import pandas as pd
import sqlite3


class MatchLoader:
    def __init__(self, data_filepath, features):
        """
        Initialize the MatchLoader with a dataset and features to extract.

        :param data: DataFrame or CSV filepath containing the match data.
        :param features: List of column names to extract as features.
        """
        self.data_filepath = data_filepath
        self.features = features
        self.conn = sqlite3.connect('MatchGuesser.db')

    def _csv_to_dataframe(self):
        """
        Convert the CSV match data to a Pandas DataFrame if needed.
        :return: A Pandas DataFrame containing the feature data
        """
        if isinstance(self.data_filepath, str):  # If data is a filepath, read the CSV
            df = pd.read_csv(self.data_filepath)
        else:
            df = self.data_filepath

        # Filter the DataFrame to include only the selected features
        return df[self.features]

    def _create_matches(self):
        """
        Group the matches by 'match_matchId' and treat each group as a separate bundle.

        :return: A list of DataFrames, each containing data for a single match.
        """
        df = self._csv_to_dataframe()

        # Group by match_matchId to create bundles
        grouped_matches = df.groupby('match_matchId')

        # Return a list of DataFrames, each representing a match
        return [group for _, group in grouped_matches]

    def _create_table(self):
        """
        Create the 'matches' table in the SQLite database if it doesn't exist already.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS matches (
            match_matchId INTEGER PRIMARY KEY,
            {", ".join([f"{col} TEXT" for col in self.features])}
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def load_matches_to_db(self):
        """
        Create a number of matches from the dataset using _create_matches function
        then add these matches to the 'matches' table within the MatchGuesser database.

        :return: A status message indicating whether the matches were successfully added to the database.
        """
        self._create_table()
        matches = self._create_matches()

        cursor = self.conn.cursor()

        # Insert matches into the database
        for match in matches:
            match_data = match[self.features].values.tolist()[0]
            match_tuple = tuple(match_data)
            placeholders = ", ".join(["?"] * len(self.features))
            query = f"INSERT OR REPLACE INTO matches ({', '.join(self.features)}) VALUES ({placeholders})"
            cursor.execute(query, match_tuple)

        self.conn.commit()
        cursor.close()

        return "Matches successfully added to the database."




# Load match data and initialize match bundler
df = pd.read_csv('../Data/lol_match_data.csv')
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]
match_bundler = MatchLoader(df, features)