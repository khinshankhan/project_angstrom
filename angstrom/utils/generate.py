import random

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
