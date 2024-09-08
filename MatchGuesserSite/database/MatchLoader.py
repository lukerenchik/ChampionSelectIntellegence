import pandas as pd
from pymongo


class MatchLoader:
    def __init__(self, data_filepath, features):
        """
        Initialize the MatchLoader with a dataset and features to extract.

        :param data_filepath: DataFrame or CSV filepath containing the match data.
        :param features: List of column names to extract as features.
        """

    def _csv_to_dataframe(self):
        """
        Convert the CSV match data to a Pandas DataFrame if needed.
        :return: A Pandas DataFrame containing the feature data
        """


    def _create_matches(self):
        """
        Group the matches by 'match_matchId' and treat each group as a separate bundle.

        :return: A list of DataFrames, each containing data for a single match.
        """


    def _create_table(self):
        """
        Create the 'matches' table in the SQLite database if it doesn't exist already.
        """


    def load_matches_to_db(self):
        """
        Create a number of matches from the dataset using _create_matches function
        then add these matches to the 'matches' table within the MatchGuesser database.

        :return: A status message indicating whether the matches were successfully added to the database.
        """



# Load match data and initialize match bundler
data_filepath = '../../Data/lol_match_data.csv'
features = [
    'match_matchId', 'player_teamId', 'player_teamPosition',
    'player_lane', 'player_champName', 'player_banPickTurn',
    'player_champName_ban', 'player_win'
]
match_bundler = MatchLoader(data_filepath, features)
match_bundler.load_matches_to_db()
