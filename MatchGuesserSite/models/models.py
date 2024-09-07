from werkzeug.security import generate_password_hash, check_password_hash
import random
from MatchGuesserSite.database.db import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    correct_counter = db.Column(db.Integer, default=0)
    incorrect_counter = db.Column(db.Integer, default=0)


    @classmethod
    def add_user(cls, username, password_hash):
        new_user = cls(
            username=username,
            password_hash=password_hash,
            correct_counter=0,
            incorrect_counter=0
        )

        db.session.add(new_user)

        try:
            db.session.commit()
            print(f"User '{username}' added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding user '{username}':", str(e))

    def __repr__(self):
        return f"<User(user_id={self.user_id}, correct_answers={self.correct_answers})>"





class MatchData(db.Model):
    __tablename__ = 'MatchData'
    __table_args__ = {'extend_existing': True}

    match_matchId = db.Column(db.String(50), nullable=False, primary_key=True)
    player_teamId = db.Column(db.String(50), nullable=False)
    player_teamPosition = db.Column(db.String(50), nullable=False)
    player_lane = db.Column(db.String(50), nullable=False)
    player_champName = db.Column(db.String(100), nullable=False)
    player_banPickTurn = db.Column(db.Integer)
    player_champName_ban = db.Column(db.String(100))
    player_win = db.Column(db.Boolean, nullable=False)


