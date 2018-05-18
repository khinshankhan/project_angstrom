'''
Stats to implement:
- Max
- Average
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

SAMPLE = {
    'test': 0
}
