import random

'''
Stats to implement:
- Max
- Num of matches
- OPR: offensive power rating (calculated from aggregated alliance scores)
- Scouted OPR (calculated from scouted information)
- DPR: defensive power rating (representative of a team's contribution to opponent's score)
  - DPRs of the two teams that comprise an alliance should add up to the opposing alliance's score
- DIm: defensive impact (subtract the cumulative OPRs of a team's opponents from the sum of the opposing scores of that team)
- CCWM: calculated contribution to winning margin (representative to how much a team helps an alliance win)
  - CCWMs of the two teams on an alliance should add to the opposing alliance's score minus their alliance's score (OPR - DPR)
- Impact: OPR - DIm
'''

from game_config import GAME_AUTO_2018 as AUTO
from game_config import GAME_TELE_2018 as TELE

# generate sample data
def generate():
    data = []
    for i in range(1, 11):
        tasks = {}

        for task in AUTO:
            task_max = AUTO[task]['max'] if AUTO[task]['max'] else 3
            tasks[task] = random.randint(AUTO[task]['min'], task_max)

        for task in TELE:
            task_max = TELE[task]['max'] if TELE[task]['max'] else 20
            tasks[task] = random.randint(TELE[task]['min'], task_max)

        data.append({
            'team': 310,
            'match': i,
            'tasks': tasks
        })

    return data

SAMPLE_SCOUT_DATA = generate()
print SAMPLE_SCOUT_DATA
s = str(SAMPLE_SCOUT_DATA).replace("'",'"')

import json
print json.dumps(json.loads(s), indent=2, sort_keys=True)

'''
START CALCULATIONS
'''

# OPR
def opr(data):
    oprs = []
    for match in data:
        opr = 0
        for task in match['tasks']:
            if 'auto' in task:
                opr += match['tasks'][task] * AUTO[task]['points']
            else:
                opr += match['tasks'][task] * TELE[task]['points']
        oprs.append(opr)
    return oprs

OPRs = opr(SAMPLE_SCOUT_DATA)
print 'Sample OPRs for each match:', OPRs
print 'Sample overall OPR:', sum(OPRs) / len(OPRs)

#
