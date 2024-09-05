from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('login.html')

@web.route('/register')
def register():
    return render_template('register.html')

@web.route('/matchguesser')
def matchguesser():
    return render_template('matchguesser.html')