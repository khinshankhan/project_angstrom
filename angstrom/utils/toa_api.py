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
def get_team_matches(key, team_num, event=None):
    '''
    Query /stations, then check through each element["teams"] and check if
    team_num is contained within it.
    For each of those matches, use /matches route to match up auton,teleop,
    endgame scores for red and blue. Now match up first half of teams listed
    with red scores and second half of teams with blue score

    if inputting event, then it should be one element from get_team_events()
    Returns the following for each match:
    [
        {
            "event_key": <string>,
            "match_key": <string>,
            "match_name": <string>,
            "event_name": <string>,
            "match_data: [
                {
                    "color": "red",
                    "teams": <list of numbers>,
                    "total": <number>,
                    "penalty": <number>,
                    "auton": <number>,
                    "teleop": <number>,
                    "endgame": <number>
                },
                {
                    "color": "blue",
                    ...
                }
            ]
        },
        ...
    ]
    '''
    res = []
    
    events = []
    if event == None:
        events = get_team_events(key, team_num)
    else:
        events = [event]
    
    for event in events:
        matches = json.loads(
                requests.get('%s/event/%s/matches'%(BASE_URL, event['event_key']),
                headers=default_header(key)).text)
        stations = json.loads(
                requests.get('%s/event/%s/matches/stations'%(BASE_URL, event['event_key']),
                headers=default_header(key)).text)
        desired_stations = []

        #find all stations in which the team_num was involved
        for station in stations:
            split_teams = map(lambda x: int(x), station["teams"].split(","))

            #if the desired team participated in this match
            if team_num in split_teams:

                #pair up with data from /matches
                for match in matches:
                    if match["match_key"] == station["match_key"]:
                        res.append({
                            "event_key": event["event_key"],
                            "match_key": match["match_key"],
                            "event_name": event["event_name"],
                            "match_name": match["match_name"],
                            "match_data": [
                                {
                                    "color": "red",
                                    "teams": split_teams[:len(split_teams)/2],
                                    "total": match["red_score"],
                                    "penalty": match["red_penalty"],
                                    "auton": match["red_auto_score"],
                                    "teleop": match["red_tele_score"],
                                    "endgame": match["red_end_score"]
                                },
                                {
                                    "color": "blue",
                                    "teams": split_teams[len(split_teams)/2:],
                                    "total": match["blue_score"],
                                    "penalty": match["blue_penalty"],
                                    "auton": match["blue_auto_score"],
                                    "teleop": match["blue_tele_score"],
                                    "endgame": match["blue_end_score"]
                                }
                            ]
                        })
    return res

