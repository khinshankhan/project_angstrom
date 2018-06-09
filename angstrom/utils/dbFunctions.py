from __future__ import print_function
import sqlite3   #enable control of an sqlite database
import copy
import os
import sys

from auth import *
from generate import *

basedir = os.path.abspath(os.path.dirname(__file__))
global db_file
db_file = basedir + "/../database.db"

# FUNCTION TO PRINT (buffer is all messed up)
def pprint(data):
    print (data,file=sys.stderr)
    return data

def db_setup():
    pprint("=========================================================")
    pprint(db_file)
    db = sqlite3.connect(db_file)
    c = db.cursor()
    querystring = """
    CREATE TABLE IF NOT EXISTS teams (
            team_num INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            robot_picture TEXT,
            members INTEGER
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE IF NOT EXISTS match_performance (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_num INTEGER,
            match_num INTEGER,
            alliance INTEGER,
            user_id INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)

    querystring = """
    CREATE TABLE IF NOT EXISTS match_tasks (
            entry_id INTEGER,
            task_name TEXT,
            count INTEGER
    );
    """
    c.execute(querystring)

    querystring = """
    CREATE TABLE IF NOT EXISTS pre_scout (
            team_num INTEGER,
            auton_prediction INTEGER,
            teleop_prediction INTEGER,
            endgame_prediction INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            permission INTEGER
    );
    """
    c.execute(querystring)

    db.commit()
    db.close()

def add_tasks_to_db(data):
    '''
        Note: as of now, tasks that were left blank on the
        form are not returned in POST data. As such, when
        you pull data from the db and a certain task is
        missing from a match, assume the team never
        accomplished that task.

        data should be in the form:
        {
                "team": <number>,
                "match": <number>,
                "alliance": (1 if blue else 0),
                "u_id": <number>,
                "tasks": {
                    task_name <string>: <number>
                },
                "notes": <string>
        }
    '''
    db = sqlite3.connect(db_file)
    c = db.cursor()

    #add other data first
    param_tuple = (data["team"], data["match"], data["alliance"], data["u_id"], data["notes"]);

    querystring = '''
        INSERT INTO match_performance (team_num, match_num, alliance, user_id, notes)
            VALUES (?, ?, ?, ?, ?);
    '''
    c.execute(querystring, param_tuple)

    #now add the tasks
    search_val = (data["team"], data["match"])  #we need the entry_id
    querystring = '''
        SELECT * FROM match_performance WHERE team_num = ? AND match_num = ?;
    '''
    c.execute(querystring, search_val)

    #get all results now, so we can access it later
    res = c.fetchall()

    #should only be one result (only want a specific team from a specific match)
    if res == None or len(res) > 1:
        #print "An error ocurred when adding match performance data, rolling back changes"
        db.rollback()
        db.close()
        return

    tasks = data["tasks"]
    for task in tasks.keys():
        param_tuple = (res[0][0], task, tasks[task])

        querystring = '''
            INSERT INTO match_tasks VALUES (?, ?, ?);
        '''
        c.execute(querystring, param_tuple)

    db.commit()
    db.close()

def valid_login(u_id, pw):
    db = sqlite3.connect(db_file)
    c = db.cursor()

    param_tuple = (u_id, hashed(pw))
    querystring = """
        SELECT user_id, password FROM users WHERE user_id = ? AND password = ?
    """
    c.execute(querystring, param_tuple)

    res = c.fetchall()
    db.close()

    if len(res) > 0:
        return True
    return False

def add_user(data):
    '''
        Data should be in format:
        {
            "u_id": <number>,
            "name": <string>,
            "password": <string>,
            "permission": <number>
        }
    '''
    # print(data, file=sys.stderr)
    # print("user fxn gets called",file=sys.stderr)
    # print(data,file=sys.stderr)
    db = sqlite3.connect(db_file)
    c = db.cursor()
    param_tuple = (
        data["u_id"],
        data["name"],
        hashed(data["password"]),
        data["permission"],
    )
    #print(param_tuple, file=sys.stderr)
    querystring = "INSERT INTO users VALUES (?, ?, ?, ?)"
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def add_pre_scout(data):
    '''
        Data should be in format:
        {
            "team": <number>,
            "auton": <number>,
            "teleop": <number>,
            "endgame": <number>
            "notes": <string>
        }
    '''
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (
            data["team"],
            data["auton"],
            data["teleop"],
            data["endgame"],
            data["notes"]
            )
    querystring = '''
        INSERT INTO pre_scout VALUES (?, ?, ?, ?, ?);
    '''
    c.execute(querystring, param_tuple)
    
    db.commit()
    db.close()

def get_pre_scout(team_num):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (team_num,)
    querystring = '''
        SELECT * FROM pre_scout WHERE team_num = ?;
    '''
    c.execute(querystring, param_tuple)
    
    db.close()

def get_user(u_id):
    db = sqlite3.connect(db_file)
    c = db.cursor()

    param_tuple = (u_id,)

    querystring = """
    SELECT user_id, name, permission FROM users WHERE user_id = ?
    """
    c.execute(querystring, param_tuple)

    temp = c.fetchall()
    if len(temp) == 0:
        #print "None found"
        return None

    db.close()
    return temp[0]

def get_users():
    db = sqlite3.connect(db_file)
    c = db.cursor()

    querystring = '''
        SELECT user_id, name, permission from users;
    '''
    c.execute(querystring)

    temp = c.fetchall()

    db.close()
    return temp

def add_team(data):
    '''
        Data should be in format:
        {
            "team": <number>,
            "team_name": <string>,
            "location": <string>,
            "num_mem": <number>,
            "pic": <string>,
        }
    '''
    # print("team fxn gets called",file=sys.stderr)
    # print(data,file=sys.stderr)
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (
        data["team"],
        data["team_name"],
        data["location"],
        data["pic"],
        data["num_mem"],
    )
    querystring = "INSERT INTO teams VALUES (?, ?, ?, ?, ?)"
    c.execute(querystring, param_tuple)

    db.commit()
    db.close()

def get_team(team_num):
    db = sqlite3.connect(db_file)
    c = db.cursor()

    param_tuple = (team_num,)
    querystring = '''
        SELECT * from teams WHERE team_num = ?;
    '''
    c.execute(querystring, param_tuple)

    temp = c.fetchall()
    if len(temp) == 0:
        #print "None found"
        return None

    #print temp

    db.close()
    return temp[0]

def get_teams():
    db = sqlite3.connect(db_file)
    c = db.cursor()

    querystring = '''
        SELECT * from teams;
    '''
    c.execute(querystring)

    temp = c.fetchall()

    db.close()
    return temp

def search_teams(query):
    db = sqlite3.connect(db_file)
    c = db.cursor()

    param_tuple = ('%' + query + '%', '%' + query + '%')
    querystring = '''
        SELECT * from teams WHERE team_num LIKE ? OR name LIKE ? ORDER BY team_num ASC;
    '''
    c.execute(querystring, param_tuple)

    temp = c.fetchall()
    db.close()
    return temp

def find_alliance_partner(team, match_num, alliance):
    db = sqlite3.connect(db_file)
    c = db.cursor()

    param_tuple = (match_num, alliance, team)
    querystring = '''
        SELECT team_num from match_performance WHERE match_num = ? AND alliance = ? AND team_num != ?;
    '''
    c.execute(querystring, param_tuple)

    temp = c.fetchall()
    if len(temp) == 0:
        #print "None found"
        return None

    #print temp[0][0]

    db.close()
    return temp[0][0]

def get_match_data(team_num, match_num):
    '''
        Note: as of now, tasks that were left blank on the
        form are not returned in POST data. As such, when
        you pull data from the db and a certain task is
        missing from a match, assume the team never
        accomplished that task.

        If results are found with the provided
        parameters, then a dictionary is returned,
        formatted as follows:
        {
                "team": <number>,
                "match": <number>,
                "alliance": (1 if blue else 0),
                "u_id": <number>,
                "tasks": {
                    task_name <string>: <number>
                },
                "notes": <string>
        }

        If no results are found, None is returned
    '''
    db = sqlite3.connect(db_file)

    db.row_factory = sqlite3.Row    #get column names
    c = db.cursor()

    res = {}

    param_tuple = (team_num, match_num);
    querystring = '''
        SELECT team_num, match_num, alliance, user_id, notes, task_name, count
            FROM (
                match_performance INNER JOIN match_tasks ON
                match_performance.entry_id = match_tasks.entry_id
            )
            WHERE team_num = ? AND match_num = ?;
    '''
    c.execute(querystring, param_tuple)
    temp = c.fetchall()

    if len(temp) == 0:
        db.close()
        return None

    res["team"] = temp[0]["team_num"]
    res["match"] = temp[0]["match_num"]
    res["alliance"] = temp[0]["alliance"]
    res["u_id"] = temp[0]["user_id"]
    res["notes"] = temp[0]["notes"]
    res["tasks"] = {}

    #now construct the task dict
    for elem in temp:
        res["tasks"][elem["task_name"]] = elem["count"]

    db.close()
    return res

def get_team_data(team_num):
    '''
        Returns a list of dictionaries, refer
        to get_match_data() for dictionary structure
    '''
    db = sqlite3.connect(db_file)
    c = db.cursor()

    #get all matches
    param_tuple = (team_num,);
    querystring = '''
        SELECT match_num FROM match_performance
            WHERE team_num = ?;
    '''
    c.execute(querystring, param_tuple)
    matches = c.fetchall()

    res = []

    for match in matches:
        res.append(get_match_data(team_num, match[0]))

    db.close()
    return res

def remove_user(u_id):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (u_id,)
    querystring = '''
        DELETE FROM users WHERE user_id = ?;
    '''
    c.execute(querystring, param_tuple)
    
    db.commit()
    db.close()

def remove_team(team_num):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (team_num,)
    querystring = '''
        DELETE FROM teams WHERE team_num = ?;
    '''
    c.execute(querystring, param_tuple)
    
    db.commit()
    db.close()

def db_setup():
    db = sqlite3.connect(db_file)
    c = db.cursor()
    querystring = """
    CREATE TABLE IF NOT EXISTS teams (
            team_num INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            robot_picture TEXT,
            members INTEGER
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE IF NOT EXISTS match_performance (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_num INTEGER,
            match_num INTEGER,
            alliance INTEGER,
            user_id INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)

    querystring = """
    CREATE TABLE IF NOT EXISTS match_tasks (
            entry_id INTEGER,
            task_name TEXT,
            count INTEGER
    );
    """
    c.execute(querystring)

    querystring = """
    CREATE TABLE IF NOT EXISTS pre_scout (
            team_num INTEGER,
            auton_prediction INTEGER,
            teleop_prediction INTEGER,
            endgame_prediction INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            permission INTEGER
    );
    """
    c.execute(querystring)

    db.commit()
    db.close()

def add_tasks_customdb(data):
    db = sqlite3.connect(db_file)
    c = db.cursor()
    param_tuple = (data["entry_id"], data["team_num"], data["match_num"], data["alliance"], data["user_id"], "none right now");

    querystring = '''
        INSERT INTO match_performance (entry_id, team_num, match_num, alliance, user_id, notes)
            VALUES (?, ?, ?, ?, ?, ?);
    '''
    c.execute(querystring, param_tuple)
    db.commit()
    
    match = generate_match(data['team_num'], data['match_num'], data['alliance'])

    querystring = '''
        INSERT INTO match_tasks (entry_id, task_name, count)
            VALUES (?, ?, ?);
    '''
    for task in match['tasks']:
        #print(i, file=sys.stderr)
        #j += i
        param_tuple = (data["entry_id"], task, match['tasks'][task]);
        c.execute(querystring, param_tuple)

    db.commit()
    db.close()

if __name__ == "__main__":
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
