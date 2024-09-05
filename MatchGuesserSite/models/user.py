from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password_hash = db.Column(db.String(200), nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    incorrect_answers = db.Column(db.Integer, default=0)

    # Relationship to track which matches the user has seen
    matches_seen = db.relationship('UserMatchSeen', backref='user', lazy=True)

    # Password hashing and verification
    def set_password(self, password):
        """Hashes the password for secure storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies a given password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register_user(password):
        """Registers a new user with a hashed password and adds them to the database."""
        user = User()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def verify_login(user_id, password):
        """Verifies if the provided user_id and password match a registered user."""
        user = User.query.filter_by(user_id=user_id).first()
        if user and user.check_password(password):
            return True
        return False

    def increment_correct_answers(self):
        """Increments the correct_answers counter for the user."""
        self.correct_answers += 1
        db.session.commit()

    def increment_incorrect_answers(self):
        """Increments the incorrect_answers counter for the user."""
        self.incorrect_answers += 1
        db.session.commit()

    def add_match_to_seen(self, match_id):
        """Adds a match to the list of matches seen by the user."""
        match_seen = UserMatchSeen(user_id=self.user_id, match_matchId=match_id)
        db.session.add(match_seen)
        db.session.commit()

    def __repr__(self):
        return f"<User(user_id={self.user_id}, correct_answers={self.correct_answers})>"


class UserMatchSeen(db.Model):
    __tablename__ = 'UserMatchSeen'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    match_matchId = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<UserMatchSeen(user_id={self.user_id}, match_matchId={self.match_matchId})>"

