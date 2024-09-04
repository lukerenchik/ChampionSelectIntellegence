import hashlib
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, password=''):
        self.username = username
        self.password = generate_password_hash(password)
        self.correct_counter = 0
        self.incorrect_counter = 0
        self.seen_matches = set()

    def _hash_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def increment_correct(self):
        """Increment the correct counter."""
        self.correct_counter += 1

    def increment_incorrect(self):
        """Increment the incorrect counter."""
        self.incorrect_counter += 1

    def save_to_db(self):
        """Save the user's data to the database."""
        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                # Check if the user already exists
                cursor.execute('SELECT * FROM users WHERE username = ?', (self.username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Update only the counters
                    cursor.execute('''
                        UPDATE users
                        SET correct_counter = ?, incorrect_counter = ?
                        WHERE username = ?
                    ''', (self.correct_counter, self.incorrect_counter, self.username))
                else:
                    # Insert new user
                    cursor.execute('''
                        INSERT INTO users (username, password, correct_counter, incorrect_counter)
                        VALUES (?, ?, ?, ?)
                    ''', (self.username, self.password, self.correct_counter, self.incorrect_counter))

                # Save seen matches (assuming 'seen_matches' table exists)
                cursor.executemany('''
                    INSERT OR IGNORE INTO seen_matches (username, match_id)
                    VALUES (?, ?)
                ''', [(self.username, match_id) for match_id in self.seen_matches])

                conn.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def load_from_db(self):
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT correct_counter, incorrect_counter FROM users WHERE username = ?', (self.username,))
            result = cursor.fetchone()
            if result:
                self.correct_counter, self.incorrect_counter = result

    def mark_match_seen(self, match_id):
        self.seen_matches.add(match_id)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO seen_matches (user_id, match_id)
            SELECT id, ? FROM users WHERE username = ?
        ''', (match_id, self.username))
        conn.commit()
        conn.close()

    def has_seen_match(self, match_id):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM seen_matches
            JOIN users ON seen_matches.user_id = users.id
            WHERE users.username = ? AND seen_matches.match_id = ?
        ''', (self.username, match_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def get_stats(self):
        total = self.correct_counter + self.incorrect_counter
        percentage = (self.correct_counter / total) * 100 if total > 0 else 0
        return {
            'correct': self.correct_counter,
            'incorrect': self.incorrect_counter,
            'percentage': percentage
        }
