from flask import Blueprint, render_template, session, redirect, url_for

web = Blueprint('web', __name__)

@web.route('/')
def index():
    # Check if the user is already logged in, and redirect to matchguesser if they are
    if 'user_id' in session:
        return redirect(url_for('web.matchguesser'))

    # Otherwise, show the login page
    return render_template('login.html')
@web.route('/register')
def register():
    return render_template('register.html')

@web.route('/matchguesser')
def matchguesser():
    # Check if the user is logged in by verifying the session
    if 'user_id' in session:
        return render_template('matchguesser.html')
    else:
        # Redirect to login if the user is not logged in
        return redirect(url_for('web.index'))