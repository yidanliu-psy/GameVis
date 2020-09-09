import pickle
import numpy as np
import statsmodels.api as sm


# find the games which are 2v2, 3v3, 4v4
def scan_game_table(table_path):
    team_game_set = set()
    target_file = open(table_path, "r")
    line = target_file.readline().strip().split(",")
    while len(line) > 1:
        game_id = int(line[0])
        game_type = str(line[1])
        if game_type in ["Doubles", "Triples", "Quadruples"]:
            team_game_set.add(game_id)
        line = target_file.readline().strip().split(",")
    return team_game_set


# store player's skill state for a given range of games
def scan_play_table(table_path, n):  # n: max games considered
    team_player_dict = {} # key: game+team; value: player id
    player_team_dict = {} # key: player id; value: game+team
    player_game_dict = {} # key: player id; value: game id
    player_skill_dict = {} # player: player id; value: player's skill level at n
    target_file = open(table_path, "r")
    line = target_file.readline().strip().split(",")

    while len(line) > 1:
        # some lines have null data fields. let's skip them 
        valid_flag = 1
        for i in range(0, 4):
            valid_flag = valid_flag * len(line[i])
        if valid_flag == 0:
            line = target_file.readline().strip().split(",")
            continue

        player_id = int(line[0])
        game_id = int(line[1])
        team_id = int(line[2])
        skill = float(line[3])
        game_num = int(line[4])
        game_team = str(game_id) + "-" + str(team_id)

        # init dicts
        team_player_dict.setdefault(game_team, set())
        player_team_dict.setdefault(player_id, set())
        player_game_dict.setdefault(player_id, set())
        
        team_player_dict[game_team].add(player_id)

        # store player's skill when n games are reached
        if len(player_team_dict[player_id]) == n - 1:
            player_skill_dict[player_id] = skill 

        # no use; skip
        if len(player_team_dict[player_id]) >= n:
            line = target_file.readline().strip().split(",")
            continue

        player_team_dict[player_id].add(game_team)
        player_game_dict[player_id].add(game_id)

        line = target_file.readline().strip().split(",")

    return team_player_dict, player_team_dict, player_game_dict, player_skill_dict


# find the most frequent teammate
def get_max_teammate(self_id, player_team_set, team_player_dict):
    teammate_dict = {}
    for game_team in player_team_set:
        for member in team_player_dict[game_team]:
            if member != self_id:
                teammate_dict.setdefault(member, 0)
                teammate_dict[member] = teammate_dict[member] + 1
    return max(teammate_dict.values())


# multivariate polyfit
def reg_m(y, x):
    x = x[::-1] # reverse list to make the right output order
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results


N = 200 # 50, 100, 200, 300, ...

team_player_dict, player_team_dict, player_game_dict, player_skill_dict = scan_play_table("play.csv", N)

team_game_set = scan_game_table("game.csv")

player_info_dict = {}

# for regression
skill_list = []
TOB_list = []
loyalty_list = []
faithfulness_list = []

for player_id in player_team_dict:
    player_team_game_set = player_game_dict[player_id] & team_game_set # only consider team games
    if (len(player_team_dict[player_id]) == N) and (len(player_team_game_set) >= 4): # min 4 games: see the PLOS ONE paper

        # calculate 4 values for regression 
        skill_list.append(player_skill_dict[player_id])
        TOB_list.append(len(player_team_game_set) / N)
        max_teammate = get_max_teammate(player_id, player_team_dict[player_id], team_player_dict)
        loyalty_list.append(max_teammate / len(player_team_game_set))
        faithfulness_list.append(max_teammate / N)
        '''
        player_info_dict[player_id] = {"TOB": len(player_team_game_set) / N}
        max_teammate = get_max_teammate(player_id, player_team_dict[player_id], team_player_dict)
        player_info_dict[player_id]["loyalty"] = max_teammate / len(player_team_game_set)
        print(player_id, player_info_dict[player_id])
        '''
print(reg_m(skill_list, [TOB_list, loyalty_list, faithfulness_list]).summary()) # regression (default: linear)




