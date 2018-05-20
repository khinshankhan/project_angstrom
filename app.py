from flask import Flask, render_template, session, redirect, url_for, flash, request
from utils.game_config import GAME_AUTO_2018 as GAME_AUTO # change to the appropiate config
from utils.game_config import GAME_TELE_2018 as GAME_TELE # change to the appropiate config

import random
import os
import sqlite3   #enable control of an sqlite database
from utils.dbFunctions import *

database = "database.db"
db = sqlite3.connect(database)
c = db.cursor()

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/')
def index():
    if 'u_id' not in session:
        return render_template('index.html')
    else:
        return redirect( url_for('home') )

@app.route('/home')
def home():
    if 'u_id' not in session:
        flash('You are not logged in.')
        return redirect( url_for('index') )
    else:
        return render_template('home.html', user=session['u_id'], GAME_AUTO = GAME_AUTO, GAME_TELE = GAME_TELE)

#will check against database later
def valid(u_id, pw):
    #if (u_id.isnumeric() and int(u_id) == 0 and pw == 'safepass'):
    if u_id.isnumeric():
        return valid_login(u_id, pw)
    return False

@app.route('/login', methods = ['POST'])
def login():
    u_id = request.form['user_id']
    pw = request.form['password']
    if valid(u_id, pw):
        session['u_id'] = int(u_id)
        return redirect( url_for('home') )
    else:
        flash('Invalid credentials.')
        return redirect( url_for('index') )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'u_id' in session:
        session.pop('u_id')
    else:
        flash('You are not logged in.')
    return redirect( url_for('index') )

@app.route('/about')
def about():
    cuser = ""
    if 'u_id' not in session:
        cuser = "Nameless Visitor"
    else:
        cuser = "User " + str(session['u_id'])
    return render_template('about.html', user=cuser)

'''
@app.route('/addmatch', methods = ['POST'])
def addmatch():
        req = requests.form
        #check for valid form, etc.
        
        #figure out how to do this?
        taskCount = 13
        
        queryString = """INSERT INTO match_performance VALUES (%d, %d, %d"""+
                ("%d," * 13)
        
        %(
                req['team-num'],
                req['match-num'],
                req['user-id'],
                #add better way to add tasks
                req['notes']
        )
        pass
'''

if __name__ == "__main__":
    app.debug = True
    db_init("database.db")

    app.run()

