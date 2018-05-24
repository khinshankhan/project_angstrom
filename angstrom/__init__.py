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
app.secret_key = "dev" #os.urandom(64)

@app.route('/')
def index():
    #temporarily disable login checks
    session['u_id'] = 0
    return redirect( url_for('home') )
    '''
    if 'u_id' not in session:
        return render_template('index.html')
    else:
        return redirect( url_for('home') )
    '''

@app.route('/home')
def home():
    if 'u_id' not in session:
        flash('You are not logged in.')
        return redirect( url_for('index') )
    else:
        return render_template('home.html', user=session['u_id'], GAME_AUTO = GAME_AUTO, GAME_TELE = GAME_TELE)

def valid(u_id, pw):
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


def gen_task_dict(form):
    task_list = {}
        
    for key in form.keys():
        temp = key.split("_")
        print "key: " +key
        print temp
        if len(temp) > 1:
            if form[key].isdigit():
                task_list[int(temp[0])] = int(form[key])
            else:
                if str(form[key]) == "on":
	            task_list[int(temp[0])] = 1
                elif str(form[key]) == "off":
	            task_list[int(temp[0])] = 0
    #add missing indices
    for x in range(0, 13):
        if not x in task_list.keys():
            task_list[x] = 0
    #print task_list
    return task_list


@app.route('/add-task', methods=['POST'])
def add_task():
    session['u_id'] = 0
    if 'u_id' not in session:
        flash('You are not logged in.')
        return redirect( url_for('index') )
    else:
        form = request.form
        #print form
        
        #alliance: blue is one, red is 0
        form_data = {
                "team": int(form["Team"]),
                "match": int(form["Match"]),
                "alliance": (1 if "Alliance" in form else 0),
                "u_id": int(session["u_id"]),
                "tasks": gen_task_dict(form),
                "notes": ("" if "Notes" not in form else form["Notes"])
	}
        add_tasks_to_db(form_data)
        
        return redirect(url_for('home'))

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')
    
if __name__ == "__main__":
    app.debug = True
    db_init("database.db")

    app.run()

