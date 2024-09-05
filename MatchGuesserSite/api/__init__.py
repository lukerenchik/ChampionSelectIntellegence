from flask import Blueprint, jsonify, request


api = Blueprint('api', __name__)


@api.route('/api/get_winning_team', methods=['GET'])
def get_winning_team():
    #May be unneccesary, returns the side of game that won (red/blue)
    pass

@api.route('/api/correct_guess', methods=['POST'])
def correct_guess():
    #Increments the users correct guesses in the database
    pass

@api.route('/api/incorrect_guess', methods=['POST'])
def incorrect_guess():
    #Increments the users incorrect guesses in the database
    pass

@api.route('/api/get_leaderboard', methods=['GET'])
def get_leaderboard():
    #Calls leaderboard class to display the top x guessers, their correct vs. incorrect, and their percentage.
    pass

@api.route('/api/rand_match', methods=['GET'])
def get_rand_match():
    """
    Get a random match from the database
    :return: a dataframe that contains match data
    """

@api.route('/api/logout', methods=['POST'])
def logout():
    #Logs the user out of their session
    pass

@api.route('/api/login', methods=['POST'])
def login():
    #Logs the user into their account
    pass

@api.route('/api/register', methods=['POST'])
def register():
    #Adds a user/pass combination to the user table in the database
    pass