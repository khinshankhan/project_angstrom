from flask import Flask, render_template, session, redirect, url_for, flash, request

from utils.game_config import GAME_AUTO_2018 as GAME_AUTO # change to the appropiate config
from utils.game_config import GAME_TELE_2018 as GAME_TELE # change to the appropiate config

import random
import os
import sqlite3   #enable control of an sqlite database
import json

# GLOBALS
database = "database.db"
db = sqlite3.connect(database)
c = db.cursor()

app = Flask(__name__)
app.secret_key = "dev" #os.urandom(64)

basedir = os.path.abspath(os.path.dirname(__file__))
team_pic_directory = "static/img/public"

from utils.dbFunctions import *
from utils.view_helper import *
from utils.stats import *

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
        print form_data
        add_tasks_to_db(form_data)
        #test = generate_all([2, 3, 4, 10], 5)
        #add_tasks_to_db(test)
        
        return redirect(url_for('home'))

@app.route('/visualize')
def visualize():
    return render_template('visualize.html', data_link = url_for('get_sample_data'))

@app.route('/profile')
def profile():
    team = {
        'team': 310,
        'team_name': 'Stuy Fission',
        'location': 'New York',
        'num_mem': 20,
        'pic': 'test.jpg',
        'notes': 'more info'
    }
    return render_template('team.html', team = team, data_link = url_for('get_310_data'))

# REQUEST ROUTES (AJAX)

@app.route('/get_310_data')
def get_310_data():
    data = generate_all([310, 1, 2, 3], 5)
    oprs = opr(data, 310)
    formatted = [{
        "id": 310,
        "values": [ [i+1, oprs[i]] for i in range(len(oprs)) ]
    }]
    return json.dumps(formatted)

@app.route('/get_sample_data')
def get_sample_data():
    json_data = open(basedir + '/static/data/data.json').read()
    data = json.loads(json_data)
    return json.dumps(data)

if __name__ == "__main__":
    app.debug = True
    db_init(database)
    app.run()
