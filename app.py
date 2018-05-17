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
    if 'u_id' not in session:
        return redirect( url_for('index') )
    else:
        return render_template('home.html', user=session['u_id'])

#will check against database later
def valid(u_id, pw):
    if (u_id.isnumeric() and int(u_id) == 0 and pw == 'safepass'):
        return True
    return False

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        u_id = request.form['user_id']
        pw = request.form['password']
        if valid(u_id, pw):
            session['u_id'] = int(u_id)
            session['pw'] = pw
            return redirect( url_for('home') )
        else:
            flash('Invalid credentials.')
            return redirect( url_for('index') )
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user')
    if 'pasa' in session:
        session.pop('pasa')
    return redirect( url_for('index') )
        
if __name__ == "__main__":
    app.debug = True
    app.run()
