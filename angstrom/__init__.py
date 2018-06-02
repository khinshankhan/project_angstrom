from __future__ import print_function
from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory

import atexit

from utils.game_config import GAME_AUTO_2018 as GAME_AUTO # change to the appropiate config
from utils.game_config import GAME_TELE_2018 as GAME_TELE # change to the appropiate config

import random
import os
import sqlite3   #enable control of an sqlite database
import json
import sys
from werkzeug.utils import secure_filename
import errno
# PATHS
basedir = os.path.abspath(os.path.dirname(__file__))
#print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",file=sys.stderr)
#print (basedir, file=sys.stderr)
#print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",file=sys.stderr)

team_pic_directory = "static/img/public"

# GLOBALS
database = basedir + "/./database.db"
global db
db = sqlite3.connect(database)
c = db.cursor()

app = Flask(__name__)
app.secret_key = "dev" #os.urandom(64)


from utils.dbFunctions import *
from utils.view_helper import *
from utils.stats import *

app.jinja_env.globals.update(is_user = is_user)
app.jinja_env.globals.update(is_admin = is_admin)


# FUNCTION TO PRINT
def aprint(data):
    print (data,file=sys.stderr)
    return data

@app.route('/')
def index():
    #temporarily disable login checks
    #session['u_id'] = 0
    #return redirect( url_for('home') )

    if not is_user():
        return render_template('index.html')
    else:
        return redirect( url_for('home') )

@app.route('/home')
@logged_in
def home():
    return render_template('home.html', GAME_AUTO = GAME_AUTO, GAME_TELE = GAME_TELE, users = get_users(), teams = get_teams())

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
    if not is_user():
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

@app.route('/pre_scout', methods=['POST'])
@logged_in
def pre_scout():
    form = request.form
    form_data = {
        "team": int(form["team_id"]),
        "auton": int(form["auton"]),
        "teleop": int(form["teleop"]),
        "endgame": int(form["endgame"]),
        "notes": form["notes"]
    }
    add_pre_scout(form_data)
    
    return redirect(url_for('home', _anchor='admin'))

@app.route('/add_teams', methods=['POST'])
@admin
def add_teams():
    if 'pic' not in request.files:
        flash('You did not upload an image.')
        return redirect(url_for('home', _anchor='admin'))

    f = request.files['pic']

    if f.filename == '':
        flash('You did not select an image.')
        return redirect(url_for('home', _anchor='admin'))

    if not allowed_file(f.filename):
        flash('Please upload a .JPG or .JPEG image.')
        return redirect(url_for('home', _anchor='admin'))

    filename = secure_filename(f.filename)
    f.save(os.path.join(team_pic_directory, filename))

    form = request.form
    form_data = {
        "team": int(form["team_num"]),
        "team_name": (form["team_name"]),
        "location": (form["location"]),
        "num_mem": (form["members"]),
        "pic": filename
        #"notes": (form["notes"])
    }
    print (form_data,file=sys.stderr)
    print('Team python checks out', file=sys.stderr)
    if get_team(int(form['team_num'])) is None:
        add_team(form_data)
        flash('Team was added.')
    else:
        flash('Team already exists.')
    return redirect(url_for('home', _anchor='admin'))

@app.route('/add_users', methods=['POST'])
@admin
def add_users():
    form = request.form
    form_data = {
        "u_id": int(form["u_id"]),
        "name": (form["name"]),
        "password": (form["password"]),
        "permission": (1 if "permission" in form else 0)
    }
    print('User python checks out', file=sys.stderr)
    if get_user(int(form['u_id'])) is None:
        add_user(form_data)
        flash('User was added.')
    else:
        flash('This user ID is already taken.')
    return redirect(url_for('home', _anchor='admin'))

@app.route('/remove_users', methods=['GET'])
@admin
def remove_users():
    u_id = int(request.args.get('u_id'))
    if get_user(u_id) is None:
        flash('User was not found.')
    else:
        remove_user(u_id)
        flash('User was removed.')
    return redirect(url_for('home', _anchor='admin'))

@app.route('/visualize')
def visualize():
    return render_template('visualize.html', data_link = url_for('get_sample_data'))

@app.route('/pictures/<filename>')
def pictures(filename):
    return send_from_directory(team_pic_directory, filename)

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

    datasets = [
        url_for('get_oprs', team_num = team_tuple[0]),
        url_for('get_impacts', team_num = team_tuple[0]),
    ]

    return render_template('team.html', team = team, team_data = team_data, oprs = oprs, impacts = impacts, datasets = datasets)

# REQUEST ROUTES (AJAX)
@app.route('/find_teams')
def get_team_item():
    teams = search_teams(request.args.get('team_num'))
    return render_template('includes/cards/team_collection.html', teams=teams)

@app.route('/get_oprs')
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

@app.route('/get_impacts')
def get_impacts():
    team_num = int(request.args.get('team_num'))
    data = get_team_data(team_num)
    impacts = impact(data, team_num)
    formatted = [{
        "id": team_num,
        "values": [ [i+1, impacts[i]] for i in range(len(impacts)) ]
    }]
    return json.dumps(formatted)

@app.route('/get_sample_data')
def get_sample_data():
    json_data = open(basedir + '/static/data/data.json').read()
    data = json.loads(json_data)
    return json.dumps(data)
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/<val>', methods=['POST','GET'])
def errors(val):
    return render_template('errors.html', error=val)
'''

def sremove(filename): #silentremove
    base = basedir[:-5] + filename
    aprint(base)
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

#exit commands
def exit_handler():
    db.close()
    sremove("database.db")
    return None

aprint ('Registering')
atexit.register(exit_handler)
aprint ('Registered')

if __name__ == "__main__":
    #sremove("database.db")
    db_setup()

    add_user({
            "u_id": 0,
            "name": "Mr. Admin",
            "password": "safepass",
            "permission": 1
        })
    add_user({
            "u_id": 10,
            "name": "Bobby",
            "password": "thisisatest",
            "permission": 1
        })
    add_user({
            "u_id": 11,
            "name": "Little Bobby",
            "password": "bobby",
            "permission": 0
        })

    add_team({
            "team": 7,
            "team_name": "Team seven",
            "location": "China",
            "num_mem": 49,
            "pic": "cool.jpg"
        })
    add_team({
            "team": 5,
            "team_name": "Team five",
            "location": "USA",
            "num_mem": 25,
            "pic": "yay.jpg"
        })
    add_team({
            "team": 100,
            "team_name": "10^2",
            "location": "USA",
            "num_mem": 10,
            "pic": "weee.jpg"
        })
    '''
    add_tasks_to_db({
            "team": <number>,
            "match": <number>,
            "alliance": (1 if blue else 0),
            "u_id": <number>,
            "tasks": {
                : <number>
            },
            "notes": <string>
        })
    '''
        

    app.debug = False
    app.run()
    #db_init(database)
        
