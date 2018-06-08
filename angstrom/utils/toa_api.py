import requests, json

BASE_URL = "https://theorangealliance.org/apiv2"

seasons = None

def default_header(key):
    return {
        "X-Application-Origin": "Project Angstrom",
        "X-TOA-Key": key
    }

def get_api_key():
    f = open('toa_key.txt')
    key = f.readline().strip()
    return key

def api_init():
    key = get_api_key()
    get_seasons(key)
    return key

def get_events(key):
    response = requests.get('%s/events'%(BASE_URL), headers=default_header(key))
    return json.loads(response.text)

def get_seasons(key):
    global seasons
    response = requests.get('%s/seasons'%(BASE_URL), headers=default_header(key))
    if seasons == None:
        seasons = json.loads(response.text)
    return json.loads(response.text)

#previous matches a team has been in
#find high score

#gets all events a team has attended
def get_team_events(key, team_num):
    for season in seasons:
        response = requests.get('%s/team/%d/%d/events'%(
                BASE_URL, team_num, int(season["season_key"])),
            headers=default_header(key))
    return json.loads(response.text)

#in the TOA api, the /matches and /stations route can be combined to find
#which teams were red or blue
#red is listed first in the station
def get_team_matches(key, team_num):
    '''
    Query /stations, then check through each element["teams"] and check if
    team_num is contained within it.
    For each of those matches, use /matches route to match up auton,teleop,
    endgame scores for red and blue. Now match up first half of teams listed
    with red scores and second half of teams with blue score
    '''
    events = get_team_events(key, team_num)
    for event in events:
        matches = json.loads(
                requests.get('%s/event/%s/matches'%(BASE_URL, event['event_key']),
                headers=default_header(key)).text)
        stations = json.loads(
                requests.get('%s/event/%s/matches/stations'%(BASE_URL, event['event_key']),
                headers=default_header(key)).text)
        found_matches = []
        for station in stations:
            if "310" in station["teams"].split(","):
                found_matches.append(station)
        print json.dumps(found_matches)

