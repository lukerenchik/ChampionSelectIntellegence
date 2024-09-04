import pandas as pd


class MatchBundler:
    def __init__(self, data, features):
        """
        Initialize the MatchBundler with a dataset and features to extract.

        :param data: DataFrame containing the match data.
        :param features: List of column names to extract as features.
        """
        self.data = data[features]
        self.features = features
        self.used_matches = set()
        self.current_index = 0
        self.bundles = self._create_bundles()

    def _create_bundles(self):
        """
        Group the matches by 'match_matchId' and treat each group as a separate bundle.

        :return: A list of DataFrames, each containing data for a single match.
        """
        grouped = self.data.groupby('match_matchId')
        bundles = [group for _, group in grouped]
        return bundles

    def get_next_bundle(self):
        """
        Return the next bundle of matches (i.e., the next single match) that hasn't been used.

        :return: DataFrame containing the data for the next match.
        """
        while self.current_index < len(self.bundles):
            bundle = self.bundles[self.current_index]
            match_id = bundle['match_matchId'].iloc[0]
            self.current_index += 1

            if match_id not in self.used_matches:
                self.used_matches.add(match_id)
                return bundle
        return None

    def reset(self):
        """
        Reset the index to start serving bundles from the beginning.
        Clear the used matches set.
        """
        self.current_index = 0
        self.used_matches.clear()
