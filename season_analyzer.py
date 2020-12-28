from espn_api.football import League
import numpy as np
from tqdm import tqdm
from collections import Counter


l = League(league_id=19854811, year=2020)

average_scores = {}
for week in tqdm(range(1,16)):
    scores = l.box_scores(week=week)
    week_scores = 0
    week_projected = 0
    for score in scores:
        week_scores += (score.home_score + score.away_score)
    average_scores[week] = (round(week_scores / 12, 3))
print(average_scores)

season_average = np.mean(list(average_scores.values()))
print(season_average)

# 1 = lucky win, -1 = unlucky loss, 0 = not lucky
def determine_luck(a_score, b_score, average):
    # wins
    if a_score == b_score:
        return 0
    if a_score > b_score:
        if (a_score > average and b_score > average) or (a_score < average and b_score < average):
            return 1
        else:
            return 0
    # loss
    else:
        if a_score > average and b_score > average or (a_score < average and b_score < average):
            return -1
        else:
            return 0


# lucky win when you score more above the average than your opponent does
                    # yourScore - average  > 0 and theirScore - average > 0 and yourScore > theirScore
# or when you score less below the average than your opponent does
                    # yourScore - average 
# unlucky loss when you score less above the average than your opponent does
                    # yourScore - average > 0 and theirScore - avearge > 0 and yourScore < theirScore
everyones_luck = {}
everyones_luck_2 = {}
team_scores = {}
for team in l.teams:
    team_scores[team] = team.scores[:-1]

for team, scores in team_scores.items():
    luck = []
    luck_2 = []
    for i, opponent in enumerate(team.schedule[:-1]):
        q = determine_luck(scores[i], team_scores[opponent][i], average_scores[i+1])
        w = determine_luck(scores[i], team_scores[opponent][i], season_average)
        luck.append(q)
        luck_2.append(w)
    everyones_luck[team] = Counter(luck)
    everyones_luck_2[team] = Counter(luck_2)


print(everyones_luck)

for team, values in everyones_luck.items():
    lwins = values[1] if 1 in values else 0
    unloss = values[-1] if -1 in values else 0
    www = f"{team.team_name} had {lwins} lucky win/s and {unloss} unlucky loss/es"
    print(www)

print("####USING A SEASON AVERAGE####")

for team, values in everyones_luck_2.items():
    lwins = values[1] if 1 in values else 0
    unloss = values[-1] if -1 in values else 0
    www = f"{team.team_name} had {lwins} lucky win/s and {unloss} unlucky loss/es"
    print(www)




