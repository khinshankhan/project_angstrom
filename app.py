from flask import Flask, render_template, session, redirect, url_for, flash, request
import random
import os
import sqlite3   #enable control of an sqlite database

database = "database.db"
db = sqlite3.connect(database)
c = db.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect( url_for('root') )
    else:
        return render_template('home.html', user=session['user'])

#will check against database later
def valid(user, pasa):
    if (user == 'admin' and  pasa == 'safepass'):
        return True
    return False

@app.route('/login', methods = ['GET', 'POST'])
def login():
    user = request.form['user']
    pasa = request.form['pass']
    result = valid(user, pasa)
    if result == True:
        session['user'] = user
        session['pasa'] = pasa
    else:
        flash('INVALID CREDENTIALS! TRY AGAIN!')
    return redirect (url_for ('root'))

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user')
    if 'pasa' in session:
        session.pop('pasa')
    return redirect( url_for('root') )
        
if __name__ == "__main__":
    app.debug = True
    app.run()
