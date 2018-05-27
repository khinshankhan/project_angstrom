import sqlite3   #enable control of an sqlite database
import copy

db_file = ""

def db_init(file_name):
    global db_file
    db_file = file_name

def db_setup():
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    querystring = """
    CREATE TABLE teams (
            team_num INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            robot_picture TEXT,
            member INTEGER,
            last_reached_worlds INTEGER
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE match_performance (
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
    CREATE TABLE match_tasks (
            entry_id INTEGER,
            task_name TEXT,
            count INTEGER
    );
    """
    c.execute(querystring)
    
    querystring = """
    CREATE TABLE pre_scout (
            team_num INTEGER,
            auton_prediction INTEGER,
            teleop_prediction INTEGER,
            endgame_prediction INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            permission INTEGER
    );
    """
    c.execute(querystring)
    db.commit()
    db.close()


def make_param_tuple(data):
    temp = []
    for key in data.keys():
        if type(data[key]) == type({}):
            for inner in data[key].keys():
                temp.append(data[key][inner])
        else:
            temp.append(data[key])
    return tuple(temp)

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
                "notes": <string or null>
	}
    '''
    global db_file
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
        print "error"   #error handle?
    
    tasks = data["tasks"]
    for task in tasks.keys():
        param_tuple = (res[0][0], task, tasks[task])
        print "param_tuple", param_tuple
        
        querystring = '''
            INSERT INTO match_tasks VALUES (?, ?, ?);
        '''
        c.execute(querystring, param_tuple)
    
    db.commit()
    db.close()

def valid_login(u_id, pw):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (u_id, pw)
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
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (
        data["u_id"],
        data["name"],
        data["password"],
        data["permission"],
    )
    querystring = "INSERT INTO users VALUES (?, ?, ?, ?)"
    
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def add_team(data):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    '''
        Data should be in format:
        {
            "team": <number>,
            "team_name": <string>,
            "location": <string>,
            "num_mem": <number>,
            "notes": <string or null>,
            "pic": <string>
        }
    '''
    param_tuple();
    querystring = "INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)"
    
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def get_team(data):
    querystring = "INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)"

if __name__ == "__main__":
    db_init("database.db")
    db_setup()

