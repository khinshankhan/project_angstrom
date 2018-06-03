import random
from dbFunctions import *

'''
Stats to implement:

DETAILED SCOUTING
- Num of matches
- Scouted OPR (calculated from scouted information)
- Expected Impact (OPR/average of alliances' OPRs)
- Impact (how much a team contributes to wins)
  - average of points scored/alliance points scored
- Reliability
  - Standard deviation of impact (smaller=more reliable)

MATCH SCORE SCOUTING
- Max
- Average
- OPR
- DPR
- DIm
- CCWM
- Impact
http://team4855.github.io/teamdata/explanation.html
'''

from game_config import GAME_AUTO_2018 as AUTO
from game_config import GAME_TELE_2018 as TELE

# generate sample data for a comp (round robin)
# takes in a list of teams
def generate_all(teams, num_matches):
    data = []
    for i in range(num_matches):
        for j in range(0, len(teams), 4):
            data.append(generate_match(teams[j], i+1, 0))
            data.append(generate_match(teams[j+1], i+1, 0))
            data.append(generate_match(teams[j+2], i+1, 1))
            data.append(generate_match(teams[j+3], i+1, 1))
            #print teams[j], teams[j+1], teams[j+2], teams[j+3]

        # do the rotation
        tmp = teams[1]
        for j in range(1, len(teams)-1):
            teams[j] = teams[j+1]
        teams[len(teams)-1] = tmp

    return data


# generate sample data for one match
def generate_match(team, match, alliance):
    tasks = {}

    for task in AUTO:
        task_max = AUTO[task]['max'] if AUTO[task]['max'] else 3
        tasks[task] = random.randint(AUTO[task]['min'], task_max)

    for task in TELE:
        task_max = TELE[task]['max'] if TELE[task]['max'] else 20
        tasks[task] = random.randint(TELE[task]['min'], task_max)

    return {
        'team': team,
        'match': match,
        'tasks': tasks,
        'alliance': alliance
    }

'''
CALCULATIONS
'''

'''
MATH
'''
# Finds the average of a list
def avg(l):
    return sum(l) / len(l)

'''
OPR

Takes in a dataset containing match data and returns the team's OPR
'''
def opr(data, team):
    oprs = []
    for match in data:
        if match['team'] == team:
            opr = 0.0
            for task in match['tasks']:
                if 'auto' in task:
                    opr += match['tasks'][task] * AUTO[task]['points']
                else:
                    #task = "['%s']"%"', '".join(task)
                    opr += match['tasks'][task] * TELE[task]['points']
            oprs.append(opr)
    return oprs

'''
Expected Impact

Takes in a dataset containing match data and returns the expected impact of a single team.
'''
def ximpact(data, team):
    team_opr = opr(data, team)
    partners_opr = [ avg(opr(data, team)) for team in alliance_partners(data, team) ]
    return avg(team_opr) / (avg(team_opr) + avg(partners_opr))


# Takes in a dataset containing all the teams' match data and returns a list of alliance partners for that team
def alliance_partners(data, team):
    return [ alliance_partner(data, team, match['match'], match['alliance']) for match in data if match['team'] == team]

# Finds a team's alliance partner in a given match
def alliance_partner(data, team, match_num, alliance):
    print get_match_data(find_alliance_partner(team, match_num, alliance), match_num)
    return get_match_data(find_alliance_partner(team, match_num, alliance), match_num)

'''
Impact

Takes in a dataset containing match data and returns a list of impacts of a single team
'''
def impact(data, team):
    team_opr = opr(data, team)
    partners_opr = [ avg(opr(data, team)) if partner else None for partner in alliance_partners(data, team) ]
    match_impacts = [ team_opr[i]/(team_opr[i] + partners_opr[i]) if partners_opr[i] else None for i in range(0,len(team_opr)) ]
    return match_impacts

'''
Reliability

Takes in a dataset containing match data and returns a value for reliability of a single team
'''
import numpy

def reliability(data, team):
    i = impact(data, team)
    return numpy.std(i)

'''
TESTING
'''

TEAMS = [1, 310, 479, 694, 1111, 2222, 3333, 4444]
SAMPLE_SCOUT_DATA = generate_all(TEAMS, len(TEAMS)-1)
s = str(SAMPLE_SCOUT_DATA).replace("'",'"')

import json
#print json.dumps(json.loads(s), indent=2, sort_keys=True)

'''
for team in TEAMS:
    o = opr(SAMPLE_SCOUT_DATA, team)
    x = ximpact(SAMPLE_SCOUT_DATA, team)
    i = impact(SAMPLE_SCOUT_DATA, team)
    r = reliability(SAMPLE_SCOUT_DATA, team)
    print 'OPRs of %d:' % team, o
    print 'Overall OPR of %d:' % team, avg(o)
    print 'Expected impact of %d:' % team, x
    print 'Impact of %d:' % team, avg(i)
    print 'Reliability of %d:' % team, r
    print
'''
