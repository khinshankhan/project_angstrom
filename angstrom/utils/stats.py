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
GLYPHS

Takes in a dataset containing match data and returns the number of glyphs a team scored
'''
def glyphs_stat(data, team):
    glyphs = []
    for match in data:
        if match['team'] == team:
            print match
            glyphs.append(match['tasks']['04_g_tele'])
    return glyphs

'''
AUTO GLYPHS

Takes in a dataset containing match data and returns the number of glyphs a team scored
'''
def auto_glyphs_stat(data, team):
    glyphs = []
    for match in data:
        if match['team'] == team:
            print match
            glyphs.append(match['tasks']['00_g_auto'])
    return glyphs

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
