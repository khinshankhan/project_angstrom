from __future__ import print_function
from flask import Flask, render_template, session, redirect, url_for, flash, request

from utils.game_config import GAME_AUTO_2018 as GAME_AUTO # change to the appropiate config
from utils.game_config import GAME_TELE_2018 as GAME_TELE # change to the appropiate config

import random
import os
import sqlite3   #enable control of an sqlite database
import json
import sys
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

app.jinja_env.globals.update(is_user = is_user)

@app.route('/')
def index():
    #temporarily disable login checks
    #session['u_id'] = 0
    #return redirect( url_for('home') )

    if 'u_id' not in session:
        return render_template('index.html')
    else:
        return redirect( url_for('home') )

@app.route('/home')
@logged_in
def home():
    perm = get_perm (session ['u_id'])
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
@logged_in
def logout():
    session.pop('u_id')
    return redirect( url_for('index') )

@app.route('/about')
def about():
    cuser = ""
    if 'u_id' not in session:
        cuser = "Nameless Visitor"
    else:
        cuser = "User " + str(session['u_id'])
    return render_template('about.html', user=cuser)

@app.route('/add_task', methods=['POST'])
@logged_in
def add_task():
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
    #print form_data
    add_tasks_to_db(form_data)
    #test = generate_all([2, 3, 4, 10], 5)
    #add_tasks_to_db(test)

    flash('Match added.')
    return redirect(url_for('home'))

@app.route('/find_team', methods=['POST'])
@logged_in
def find_team():
    team_num = search_team(request.form['search_team'])
    if team_num is None:
        flash('Team was not found.')
        return redirect(url_for('home', _anchor='dashboard'))
    return redirect(url_for('profile', team_num = team_num))

@app.route('/add_teams', methods=['POST'])
@logged_in
def add_teams():
    form = request.form
    form_data = {
        "team": int(form["team_num"]),
        "team_name": (form["team_name"]),
        "location": (form["location"]),
        "num_mem": (form["members"]),
        "pic": (form["pic"])
        #"notes": (form["notes"])
    }
    print (form_data,file=sys.stderr)
    print('Team python checks out', file=sys.stderr)
    add_team(form_data)
    flash('Team was added.')
    return redirect(url_for('home', _anchor='admin'))

@app.route('/add_users', methods=['POST'])
@logged_in
def add_users():
    form = request.form
    form_data = {
        "u_id": int(form["u_id"]),
        "name": (form["name"]),
        "password": (form["password"]),
        "permission": (1 if "permission" in form else 0)
    }
    print (form_data,file=sys.stderr)
    print('User python checks out', file=sys.stderr)
    add_user(form_data)
    flash('User was added.')
    return redirect(url_for('home', _anchor='admin'))

@app.route('/visualize')
def visualize():
    return render_template('visualize.html', data_link = url_for('get_sample_data'))

@app.route('/profile')
@logged_in
def profile():
    if not request.args['team_num']:
        flash('Team was not found.')
        return redirect(url_for('home', _anchor='dashboard'))

    team_tuple = get_team(int(request.args['team_num']))
    team = {
        'team': team_tuple[0],
        'team_name': team_tuple[1],
        'location': team_tuple[2],
        'num_mem': team_tuple[4],
        'pic': team_tuple[3]
    }

    team_data = get_team_data(team_tuple[0])
    oprs = opr(team_data, team_tuple[0])
    impacts = impact(team_data, team_tuple[0])

    return render_template('team.html', team = team, team_data = team_data, oprs = oprs, impacts = impacts, data_link = url_for('get_oprs', team_num = team_tuple[0]))

# REQUEST ROUTES (AJAX)

@app.route('/get_opr')
def get_oprs():
    team_num = int(request.args.get('team_num'))
    data = get_team_data(team_num)
    oprs = opr(data, team_num)
    formatted = [{
        "id": team_num,
        "values": [ [i+1, oprs[i]] for i in range(len(oprs)) ]
    }]
    #print data
    return json.dumps(formatted)

@app.route('/get_sample_data')
def get_sample_data():
    json_data = open(basedir + '/static/data/data.json').read()
    data = json.loads(json_data)
    return json.dumps(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True
    app.run()
    #db_init(database)
