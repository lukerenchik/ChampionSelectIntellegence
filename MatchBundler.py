import pandas as pd


class MatchBundler:
    def __init__(self, data, features):
        """
        Initialize the MatchBundler with a dataset and features to extract.

        :param data: DataFrame containing the match data.
        :param features: List of column names to extract as features.
        """
        self.data = data[features]  # Only keep the relevant features
        self.features = features
        self.bundles = self._create_bundles()
        self.current_index = 0

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
        Return the next bundle of matches (i.e., the next single match).

        :return: DataFrame containing the data for the next match.
        """
        if self.current_index < len(self.bundles):
            bundle = self.bundles[self.current_index]
            self.current_index += 1
            return bundle
        else:
            return None  # No more bundles left

    def reset(self):
        """
        Reset the index to start serving bundles from the beginning.
        """
        self.current_index = 0


