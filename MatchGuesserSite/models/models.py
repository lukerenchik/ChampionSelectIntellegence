import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, user_id=None, username=None, password_hash=None, correct_counter=0, incorrect_counter=0):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.correct_counter = correct_counter
        self.incorrect_counter = incorrect_counter

    @staticmethod
    def create_table():
        with sqlite3.connect('MatchGuesser.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                correct_counter INTEGER DEFAULT 0,
                incorrect_counter INTEGER DEFAULT 0
            )''')
            conn.commit()

    @staticmethod
    def add_user(username, password_hash):
        try:
            with sqlite3.connect('MatchGuesser.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO users (username, password_hash, correct_counter, incorrect_counter)
                                  VALUES (?, ?, 0, 0)''', (username, password_hash))
                conn.commit()
                print(f"User '{username}' added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error adding user '{username}':", str(e))

    @staticmethod
    def get_user_by_username(username):
        with sqlite3.connect('MatchGuesser.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    def __repr__(self):
        return f"<User(user_id={self.user_id}, correct_answers={self.correct_counter}, incorrect_answers={self.incorrect_counter})>"



