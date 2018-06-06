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


