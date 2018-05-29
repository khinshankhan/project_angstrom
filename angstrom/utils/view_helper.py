from functools import wraps
from flask import session, redirect, url_for, flash
from dbFunctions import *

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

