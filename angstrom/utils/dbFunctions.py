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
            members INTEGER
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
        print "An error ocurred when adding match performance data, rolling back changes"
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
            "pic": <string>,
        }
    '''
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
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (team_num,)
    querystring = '''
        SELECT * from teams WHERE team_num = ?;
    '''
    c.execute(querystring, param_tuple)
    
    temp = c.fetchall()
    if len(temp) == 0:
        print "None found"
        return None
    
    print temp
    
    db.close()
    return temp[0]

def search_team(query):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (query, '%' + query + '%')
    querystring = '''
        SELECT team_num from teams WHERE team_num = ? OR name LIKE ?;
    '''
    c.execute(querystring, param_tuple)
    
    temp = c.fetchall()
    if len(temp) == 0:
        print "None found"
        return None
    
    print temp
    
    db.close()
    return temp[0]

def find_alliance_partner(team, match_num, alliance):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (match_num, alliance, team)
    querystring = '''
        SELECT team_num from match_performance WHERE match_num = ? AND alliance = ? AND team_num != ?;
    '''
    c.execute(querystring, param_tuple)
    
    temp = c.fetchall()
    if len(temp) == 0:
        print "None found"
        return None
    
    print temp[0][0]
    
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
    
    global db_file
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
    global db_file
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

if __name__ == "__main__":
    db_init("database.db")
    db_setup()
    #get_match_data(1, 1)
    '''
    add_team({
            "team": 7,
            "team_name": "Team seven",
            "location": "China",
            "num_mem": 49,
            "pic": "cool.jpg",
            "worlds": 2011
        })
    get_team(7)
    
    add_user({
            "u_id": 0,
            "name": "Mr. Admin",
            "password": "safepass",
            "permission": 0
        })
    '''
    #get_team_data(1)

