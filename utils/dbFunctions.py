import sqlite3   #enable control of an sqlite database

db = None
c = None

def init(db_file):
	db = sqlite3.connect(db_file)
	c = db.cursor()

def setup():
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
		team_num INTEGER,
		match_num INTEGER,
		user_id INTEGER,
		task_1 INTEGER,
		task_2 INTEGER,
		task_3 INTEGER,
		task_4 INTEGER,
		task_5 INTEGER,
		task_6 INTEGER,
		task_7 INTEGER,
		task_8 INTEGER,
		task_9 INTEGER,
		task_10 INTEGER,
		task_11 INTEGER,
		task_12 INTEGER,
		task_13 INTEGER,
		notes TEXT
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

def db_close():
	db.close();



