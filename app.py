from flask import Flask, render_template, session, redirect, url_for, flash,request
import random
import os

app = Flask(__name__)

@app.route('/')
def root():
    if(loggedin()):
        return "home.html"
    else:
        return "fake.html"

def loggedin():
    if ('user' in session and 'pass' in session):
        if (valid(session['user']) and valid(session['pass'])):
            return True
    return False

#will check against database later
def valid():
    if (session['user'] == 'admin' and  session['pass'] == 'safepass'):
        return True
    return False

@app.route('/login', methods = ['GET', 'POST'])
def login():
    session['user'] = request.form['user']
    session['pass'] = request.form['pass']
    return redirect (url_for ('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()
