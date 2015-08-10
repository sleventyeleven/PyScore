from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)

from lib import *

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form.get('username'),
                        request.form.get('password')):
            flash("Succesfully logged in")
            return redirect(url_for('welcome', username=request.form.get('username')))
        else:
            error = "Incorrect username and password"
    return render_template('login.html', error=error)

@app.route('/register')
def register():
    return render_template('register.html', methods=['POST', 'GET'])
	error = None
    if request.method == 'POST':
        if register_user(request.form.get('username'), request.form.get('password1'), request.form.get('password2'), request.form.get('email'), request.form.get('g-recaptcha-response')):
            flash("Succesfully registered")
            return redirect(url_for('challenges', username=request.form.get('username')))
        else:
            error = "Incorrect username and password"
    return render_template('login.html', error=error)
	
@app.route('/score')
def score():
    return render_template('score.html')
	
@app.route('/logout')
def logout(username):
    return render_template('challenges.html')
	
@app.route('/challenges')
def challenges(username):
    return render_template('challenges.html', username=username, total=total)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SuperSecretKey'
    app.run()
