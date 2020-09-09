import pickle
import numpy as np


# build dict to store the ids of three types of games
def scan_game_table(table_path):
    team_game_dict = {"Doubles": {}, "Triples": {}, "Quadruples": {}}
    target_file = open(table_path, "r")
    line = target_file.readline().strip().split(",")
    while len(line) > 1:
        game_id = int(line[0])
        game_type = str(line[1])

        if game_type in ["Doubles", "Triples", "Quadruples"]:
            team_game_dict[game_type][game_id] = {1: [], 2: []}
        line = target_file.readline().strip().split(",")
    return team_game_dict


# store the team and player imformation of each game
def fill_game_dict(table_path, game_dict):
    target_file = open(table_path, "r")
    line = target_file.readline().strip().split("\t")

    error_game_set = set() # some games have >2 teams; will be filtered out

    while len(line) > 1:
        try:
            player_id = int(line[0])
            game_id = int(line[1])
            team_id = int(line[2])
            old_new_skill = (float(line[3]), float(line[4])) # concatenate old and new games to simplify the structure
        except ValueError: # handle null data field in some lines
            line = target_file.readline().strip().split("\t")
            continue

        for game_type in ["Doubles", "Triples", "Quadruples"]:
            if game_id in game_dict[game_type].keys():
                if team_id > 2:
                    error_game_set.add(game_id) # >2 teams
                else:
                    game_dict[game_type][game_id][team_id].append(old_new_skill)
                continue
        line = target_file.readline().strip().split("\t")
    return game_dict, error_game_set


# calculate [delta, I, T, O] for each game
def gen_subtable(game, team_vol):
    rows = []
    if len(game[1]) == len(game[2]) == team_vol:
        # add up *total* skill levels for two teams
        old_skills = {1: 0, 2: 0} 
        for team_id in [1, 2]:
            for player_id in range(team_vol):
                old_skills[team_id] = old_skills[team_id] + game[team_id][player_id][0]
        # team by team
        for team_id in [1, 2]:
            # player by player
            for player_id in range(team_vol):
                center_old_skill = game[team_id][player_id][0]
                center_new_skill = game[team_id][player_id][1]

                # get average
                teammate_old_skill = (old_skills[team_id] - center_old_skill) / (team_vol - 1)
                opponent_old_skill = old_skills[3 - team_id] / team_vol # team switcher: 1=3-2, 2=3-1

                rows.append([center_new_skill - center_old_skill, center_old_skill, teammate_old_skill, opponent_old_skill])
    else:
        None 
    return rows


# get table for each game type: line by line
def gen_table(game_type, game_dict, error_game_set):
    valid_table = []
    if game_type == "Doubles":
        team_vol = 2
    elif game_type == "Triples":
        team_vol = 3
    elif game_type == "Quadruples":
        team_vol = 4
    else:
        print("???")
    for game_id in set(game_dict[game_type]) - error_game_set: # filter
        valid_table = valid_table + gen_subtable(game_dict[game_type][game_id], team_vol)
    return valid_table


game_dict = scan_game_table("game.csv")
game_dict, error_game_set = fill_game_dict("old_new.txt", game_dict)
print("done")
# warning: very *time-consuming*!!!
for game_type in ["Doubles", "Triples", "Quadruples"]:
    pickle.dump(gen_table(game_type, game_dict, error_game_set), open(game_type + "_table.pkl", "wb"))