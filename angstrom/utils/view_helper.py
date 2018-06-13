from functools import wraps
from flask import session, redirect, url_for, flash
from dbFunctions import *

from num2words import *
import random

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

        add_user({"u_id": 0, "name": "Mr. Admin", "password": "safepass", "permission": 1})
        add_user({"u_id": 10, "name": "Bobby", "password": "thisisatest","permission": 1})
        add_user({"u_id": 11, "name": "Little Bobby", "password": "bobby", "permission": 0 })

        for i in range(1,10):
            add_user({"u_id": i, "name": "tuser" + str(i), "password": "test" + str(i), "permission": 0})

        add_team({
            "team": 7,
            "team_name": "Team seven",
            "location": "China",
            "num_mem": 49,
            "pic": "itsa.jpg"
        })
        add_team({
            "team": 5,
            "team_name": "Team five",
            "location": "USA",
            "num_mem": 25,
            "pic": "itsa.jpg"
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
        add_pre_scout({
            "team": 7,
            "auton": 50,
            "teleop": 150,
            "endgame": 20,
            "notes": "Pretty well made robot."
        })
        add_pre_scout({
            "team": 5,
            "auton": 10,
            "teleop": 200,
            "endgame": 0,
            "notes": ""
        })
        country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
        semaphore = 0
        doublesemaphore = 0
        entry = 7
        match = 4
        for i in range(17,25):
            country = random.randint(1,len(country_list)-1)
            add_team({
                "team": i,
                "team_name": "Team " + num2word(i),
                "location": country_list[country],
                "num_mem": random.randint(1,101),
                "pic": "itsa.jpg"
            })
            add_tasks_customdb({
                "entry_id": entry,
                "team_num": i,
                "match_num": match,
                "alliance": semaphore,
                "user_id": 0,
            })
            entry += 1
            add_tasks_customdb({
                "entry_id": entry,
                "team_num": i,
                "match_num": match + 1,
                "alliance": semaphore,
                "user_id": 0,
            })
            entry += 1
            add_tasks_customdb({
                "entry_id": entry,
                "team_num": i,
                "match_num": match + 2,
                "alliance": semaphore,
                "user_id": 0,
            })
            entry += 1
            add_tasks_customdb({
                "entry_id": entry,
                "team_num": i,
                "match_num": match + 3,
                "alliance": semaphore,
                "user_id": 0,
            })
            entry += 1
            add_pre_scout({
                "team": i,
                "auton": random.randint(1,30),
                "teleop": random.randint(100,301),
                "endgame": 0,
                "notes": ""
            })
            doublesemaphore += 1
            if semaphore == 1 and doublesemaphore == 3:
                match += 4
            if doublesemaphore == 4:
                doublesemaphore = 0
            if semaphore == 1:
                semaphore = 0
            else:
                semaphore = 1
                

if __name__ == "__main__":
    db_setup()
    add_sample()
