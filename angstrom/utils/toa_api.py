import requests

BASE_URL = "https://theorangealliance.org/apiv2"

def get_api_key():
    f = open('toa_key.txt')
    key = f.readline().strip()
    return key

def get_events(key):
    headers = {
        "X-Application-Origin": "Project Angstrom",
        "X-TOA-Key": key
    }
    response = requests.get('%s/events'%(BASE_URL), headers=headers)
    return response.text

def 

#previous matches a team has been in
#find high score
