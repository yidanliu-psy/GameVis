# 玩第100, 200, ..., 1300局的时候
# 按人，记录skill
# loyalty: 过去100？n？场 最多人次数/总组队次数
# TOB：总组队次数/总次数

# 通过game表，可以获得team_game_set

# 扫描play表，生成字典{team_game_id_team_id: player_id_set}；（在指定总局数时）生成字典{player_id: game_id_set_team_id}

# 对于每个player，（记得过滤总局数不足的）
# - 局数=指定超参
# - 团体局=team_game_set ∩ player_game_set (如果len<4，排除)
# - 最铁队友局数=扫描团体局，生成字典{teammate_id: number}；输出最大的number

import pickle
import numpy as np
import statsmodels.api as sm


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
    # pickle.dump(team_game_set, open("team_game_set.pkl", "wb"))


def scan_play_table(table_path, n):  # n: max games considered
    team_player_dict = {}
    player_team_dict = {}
    player_game_dict = {}
    player_skill_dict = {}
    target_file = open(table_path, "r")
    line = target_file.readline().strip().split(",")

    while len(line) > 1:
        valid_flag = 1
        for i in range(0, 4):
            valid_flag = valid_flag * len(line[i])
        if valid_flag == 0:
            # print(line)
            line = target_file.readline().strip().split(",")
            continue

        player_id = int(line[0])
        game_id = int(line[1])
        team_id = int(line[2])
        skill = float(line[3])
        game_num = int(line[4])

        game_team = str(game_id) + "-" + str(team_id)
        team_player_dict.setdefault(game_team, set())
        team_player_dict[game_team].add(player_id)

        player_team_dict.setdefault(player_id, set())
        player_game_dict.setdefault(player_id, set())

        if len(player_team_dict[player_id]) == n - 1:
            player_skill_dict[player_id] = skill

        if len(player_team_dict[player_id]) >= n:
            line = target_file.readline().strip().split(",")
            continue

        player_team_dict[player_id].add(game_team)
        player_game_dict[player_id].add(game_id)

        line = target_file.readline().strip().split(",")

    return team_player_dict, player_team_dict, player_game_dict, player_skill_dict


def get_max_teammate(self_id, player_team_set, team_player_dict):
    teammate_dict = {}
    for game_team in player_team_set:
        for member in team_player_dict[game_team]:
            if member != self_id:
                teammate_dict.setdefault(member, 0)
                teammate_dict[member] = teammate_dict[member] + 1
    return max(teammate_dict.values())


def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

N = 200

team_player_dict, player_team_dict, player_game_dict, player_skill_dict = scan_play_table("play.csv", N)
pickle.dump((team_player_dict, player_team_dict, player_game_dict), open("100.pkl", "wb"))

team_game_set = scan_game_table("game.csv")

player_info_dict = {}

skill_list = []
TOB_list = []
loyalty_list = []
faithfulness_list = []

for player_id in player_team_dict:
    player_team_game_set = player_game_dict[player_id] & team_game_set
    if (len(player_team_dict[player_id]) == N) and (len(player_team_game_set) >= 4):
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
print(reg_m(skill_list, [TOB_list, loyalty_list, faithfulness_list]).summary())
# pickle.dump((skill_list, TOB_list, loyalty_list, faithfulness_list), open(str(N) + ".pkl", "wb"))




