from functools import wraps
from flask import session, redirect, url_for, flash
from dbFunctions import *

basedir = os.path.abspath(os.path.dirname(__file__))
global db_file
db_file = basedir + "/../database.db"

def logged_in(f):
    @wraps(f)
    def check_user(*args, **kwargs):
        if not 'u_id' in session:
            flash('You are not logged in.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return check_user

def admin(f):
    @wraps(f)
    def check_user(*args, **kwargs):
        if not is_user():
            flash('You are not logged in.')
            return redirect(url_for('index'))
        elif not is_admin():
            flash('You do not have permission to view this page.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return check_user

def is_user():
    return 'u_id' in session

def is_admin():
    # get user and check if admin
    if is_user():
        return get_user(session['u_id'])[2] == 1
    else:
        return False

def valid(u_id, pw):
    if u_id.isnumeric():
        return valid_login(u_id, pw)
    return False

def allowed_file(filename):
        return '.' in filename and \
                       filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg']

def extract_task_id(tasks):
    '''
        tasks is a dict
    '''
    

def gen_task_dict(form):
    task_list = {}
        
    for key in form.keys():
        temp = key.split("_")
        if len(temp) > 1:
            if form[key].isdigit():
                task_list[key] = int(form[key])
            else:
                if str(form[key]) == "on":
	            task_list[key] = 1
                elif str(form[key]) == "off":
	            task_list[key] = 0
    '''
    #add missing indices
    for x in range(0, 13):
        if not x in task_list.keys():
            task_list[x] = 0
    '''
    return task_list


def add_sample():
    if not os.path.isfile(db_file):
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
        add_tasks_customdb({
                    "entry_id": 1,
                    "team_num": 5,
                    "match_num": 1,
                    "alliance": 1,
                    "user_id": 0,
                })
        add_tasks_customdb({
                    "entry_id": 2,
                    "team_num": 5,
                    "match_num": 2,
                    "alliance": 1,
                    "user_id": 0,
                })
        add_tasks_customdb({
                    "entry_id": 3,
                    "team_num": 5,
                    "match_num": 3,
                    "alliance": 1,
                    "user_id": 0,
                })
        add_tasks_customdb({
                    "entry_id": 4,
                    "team_num": 7,
                    "match_num": 1,
                    "alliance": 1,
                    "user_id": 0,
                })
        add_tasks_customdb({
                    "entry_id": 5,
                    "team_num": 7,
                    "match_num": 2,
                    "alliance": 1,
                    "user_id": 0,
                })
        add_tasks_customdb({
                    "entry_id": 6,
                    "team_num": 7,
                    "match_num": 3,
                    "alliance": 1,
                    "user_id": 0,
                })

if __name__ == "__main__":
    db_setup()
    add_sample()
