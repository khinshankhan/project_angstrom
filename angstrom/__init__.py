#necessary imports for app (literally can't operate without)
from __future__ import print_function
from flask import Flask, render_template, session, redirect, url_for, flash, request, send_from_directory
from werkzeug.utils import secure_filename
#imports from other files (files we made to keep everything organized and clean)
from utils.game_config import GAME_AUTO_2018 as GAME_AUTO # change to the appropiate config
from utils.game_config import GAME_TELE_2018 as GAME_TELE # change to the appropiate config
from utils.dbFunctions import *
from utils.view_helper import *
from utils.toa_api import *
from utils.stats import *
#imports for logistics (makes stuff happen, eg read or open db)
import random
import os
import sqlite3 #enable control of an sqlite database
import json
import sys
#extra imports (not needed, but help make the app smooth)
import errno
import logging
import atexit

# FUNCTION TO PRINT (buffer is all messed up)
def aprint(data):
    print (data,file=sys.stderr)
    return data
'''
#custom file remover
def sremove(filename): #silentremove
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
'''

# PATHS
basedir = os.path.abspath(os.path.dirname(__file__))
team_pic_directory = "static/img/public"

add_sample()

#naming of app and key
app = Flask(__name__)
app.secret_key = "keysmithsmakekeys" #os.urandom(64)

#global, continuously updating variables using functions
app.jinja_env.globals.update(is_user = is_user)
app.jinja_env.globals.update(is_admin = is_admin)
app.jinja_env.globals.update(get_user = get_user)

@app.route('/')
def index():
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
        cuser = "Mysterious Visitor"
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
    if get_team(form_data['team']) is not None:
        add_tasks_to_db(form_data)
        flash('Match added.')
    else:
        flash('This team is not currently competing.')
    #test = generate_all([2, 3, 4, 10], 5)
    #add_tasks_to_db(test)

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
    if request.args:
        qs_teams = request.args.getlist("teams")
        teams_to_display = [ get_team(t)[0] for t in qs_teams ]
    else:
        teams_to_display = []
    teams = get_teams()

    datasets = [
        url_for('get_oprs', team_nums = teams_to_display),
        url_for('get_impacts', team_nums = teams_to_display)
    ]

    return render_template('visualize.html', teams = teams, datasets = datasets, team_nums = teams_to_display)

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
        url_for('get_oprs', team_nums = [team_tuple[0]]),
        url_for('get_impacts', team_nums = [team_tuple[0]]),
        url_for('get_glyphs', team_nums = [team_tuple[0]]),
        url_for('get_auto_glyphs', team_nums = [team_tuple[0]])
    ]

    return render_template('team.html', team = team, team_data = team_data, oprs = oprs, impacts = impacts, datasets = datasets)

# REQUEST ROUTES (AJAX)
@app.route('/find_teams')
def get_team_item():
    teams = search_teams(request.args.get('team_num'))
    return render_template('includes/cards/team_collection.html', teams=teams)

@app.route('/get_oprs')
def get_oprs():
    team_nums = request.args.getlist('team_nums')

    # loop through team nums and append data to data key
    data_fields = []
    for team in team_nums:
        team = int(team)
        data = get_team_data(team)
        oprs = opr(data, team)

        data_field = {
            "id": team,
            "values": [ [i+1, oprs[i]] for i in range(len(oprs)) ]
        }
        data_fields.append(data_field)

    formatted = {
        "name": "OPR",
        "data": data_fields
    }

    return json.dumps(formatted)

@app.route('/get_impacts')
def get_impacts():
    team_nums = request.args.getlist('team_nums')

    # loop through team nums and append data to data key
    data_fields = []
    for team in team_nums:
        team = int(team)
        data = get_team_data(team)
        impacts = impact(data, team)

        data_field = {
            "id": team,
            "values": [ [i+1, impacts[i]] for i in range(len(impacts)) ]
        }
        data_fields.append(data_field)

    formatted = {
        "name": "Impact",
        "data": data_fields
    }

    return json.dumps(formatted)

@app.route('/get_glyphs')
def get_glyphs():
    team_nums = request.args.getlist('team_nums')

    # loop through team nums and append data to data key
    data_fields = []
    for team in team_nums:
        team = int(team)
        data = get_team_data(team)
        glyphs = glyphs_stat(data, team)

        data_field = {
            "id": team,
            "values": [ [i+1, glyphs[i]] for i in range(len(glyphs)) ]
        }
        data_fields.append(data_field)

    formatted = {
        "name": "Total Glyphs",
        "data": data_fields
    }

    return json.dumps(formatted)

@app.route('/get_auto_glyphs')
def get_auto_glyphs():
    team_nums = request.args.getlist('team_nums')

    # loop through team nums and append data to data key
    data_fields = []
    for team in team_nums:
        team = int(team)
        data = get_team_data(team)
        auto_glyphs = auto_glyphs_stat(data, team)

        data_field = {
            "id": team,
            "values": [ [i+1, auto_glyphs[i]] for i in range(len(auto_glyphs)) ]
        }
        data_fields.append(data_field)

    formatted = {
        "name": "Auto Glyphs",
        "data": data_fields
    }

    return json.dumps(formatted)

def get_api_key():
    f = open('toa_key.txt')
    key = f.readline().strip()
    return key

#custom whatever page
'''
@app.route('/<val>', methods=['POST','GET'])
def errors(val):
    #status_as_integer = response.status_code
    return render_template('errors.html', error=val, status=stat)
'''
#custom error pages
@app.errorhandler(404)
def page_error__404(error):
        return render_template('errors.html', error=error, status=404), 404
@app.errorhandler(405)
def page_error__405(error):
        return render_template('errors.html', error=error, status=405), 405
@app.errorhandler(406)
def page_error__406(error):
        return render_template('errors.html', error=error, status=406), 406
@app.errorhandler(408)
def page_error__408(error):
        return render_template('errors.html', error=error, status=408), 408
@app.errorhandler(409)
def page_error__409(error):
        return render_template('errors.html', error=error, status=409), 409
@app.errorhandler(410)
def page_error__410(error):
        return render_template('errors.html', error=error, status=410), 410
@app.errorhandler(411)
def page_error__411(error):
        return render_template('errors.html', error=error, status=411), 411
@app.errorhandler(412)
def page_error__412(error):
        return render_template('errors.html', error=error, status=412), 412
@app.errorhandler(413)
def page_error__413(error):
        return render_template('errors.html', error=error, status=413), 413
@app.errorhandler(414)
def page_error__414(error):
        return render_template('errors.html', error=error, status=414), 414
@app.errorhandler(415)
def page_error__415(error):
        return render_template('errors.html', error=error, status=415), 415
@app.errorhandler(416)
def page_error__416(error):
        return render_template('errors.html', error=error, status=416), 416
@app.errorhandler(417)
def page_error__417(error):
        return render_template('errors.html', error=error, status=417), 417
@app.errorhandler(428)
def page_error__428(error):
        return render_template('errors.html', error=error, status=428), 428
@app.errorhandler(429)
def page_error__429(error):
        return render_template('errors.html', error=error, status=429), 429
@app.errorhandler(431)
def page_error__431(error):
        return render_template('errors.html', error=error, status=431), 431
@app.errorhandler(500)
def page_error__500(error):
        return render_template('errors.html', error=error, status=500), 500
@app.errorhandler(501)
def page_error__501(error):
        return render_template('errors.html', error=error, status=501), 501
@app.errorhandler(502)
def page_error__502(error):
        return render_template('errors.html', error=error, status=502), 502
@app.errorhandler(503)
def page_error__503(error):
        return render_template('errors.html', error=error, status=503), 503
@app.errorhandler(504)
def page_error__504(error):
        return render_template('errors.html', error=error, status=504), 504
@app.errorhandler(505)
def page_error__505(error):
        return render_template('errors.html', error=error, status=505), 505


'''    
#exit commands
def exit_handler():
    aprint("Exiting")
    db.close()
    sremove(database)
    return None

#connects exit handler to the app
aprint ('Registering')
atexit.register(exit_handler)
aprint ('Registered')
'''

#logs app reponses into console
'''
@app.after_request
def log_the_status_code(response):
    status_as_string = response.status
    status_as_integer = response.status_code
    logging.warning("status as string %s" % status_as_string)
    logging.warning("status as integer %s" % status_as_integer)
    global stat
    stat = status_as_integer
    return response
'''

if __name__ == "__main__":
    app.debug = False
    get_events(get_api_key())
    app.run()

