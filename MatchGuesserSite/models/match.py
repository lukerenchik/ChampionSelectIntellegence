import random
from flask_sqlalchemy import SQLAlchemy
from user import UserMatchSeen

db = SQLAlchemy()

class MatchData(db.Model):
    __tablename__ = 'MatchData'

    match_matchId = db.Column(db.Integer, nullable=False, primary_key=True)
    player_teamId = db.Column(db.Integer, nullable=False)
    player_teamPosition = db.Column(db.String(50), nullable=False)
    player_lane = db.Column(db.String(50), nullable=False)
    player_champName = db.Column(db.String(100), nullable=False)
    player_banPickTurn = db.Column(db.Integer)
    player_champName_ban = db.Column(db.String(100))
    player_win = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def get_random_unseen_match(user_id):
        """
        Returns a random match that the user has not already seen.

        :param user_id: The ID of the user for whom we want to find an unseen match.
        :return: A random MatchData object representing an unseen match.
        """
        # Get the match IDs that the user has already seen
        seen_matches = db.session.query(UserMatchSeen.match_matchId).filter_by(user_id=user_id).all()
        seen_match_ids = [match.match_matchId for match in seen_matches]

        # Query all matches that are not in the list of seen match IDs
        unseen_matches = MatchData.query.filter(~MatchData.match_matchId.in_(seen_match_ids)).all()

        # Return a random unseen match, or None if no unseen matches are available
        if unseen_matches:
            return random.choice(unseen_matches)
        return None

    def __repr__(self):
        return f"<MatchData(match_matchId={self.match_matchId}, player_teamId={self.player_teamId})>"
