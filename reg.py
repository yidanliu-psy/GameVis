import pickle
import numpy as np
import statsmodels.api as sm
import sys


def outlier(oneD):
    q75, q25 = np.percentile(oneD, [75, 25])
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return np.multiply(oneD < upper, oneD > lower)

def reg_m(y, x):
    x = x[::-1]
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results


def poly(mat, order=1):
    teammate0 = mat[2] / mat[1]
    opponent0 = mat[3] / mat[1]
    valid_mask = np.multiply(outlier(mat[0]), outlier(teammate0), outlier(opponent0))



    teammate0 = teammate_list = teammate0[valid_mask]
    opponent0 = opponent_list = opponent0[valid_mask]

    # np.save("save.npy", np.concatenate((mat[0][valid_mask], teammate0, opponent0)).reshape(3, len(teammate0)))

    for i in range(2, order + 1):
        teammate_list = np.concatenate((teammate_list, np.power(teammate0, i)))
        opponent_list = np.concatenate((opponent_list, np.power(opponent0, i)))

    dep_val = np.concatenate((teammate_list, opponent_list)).reshape(order * 2, len(teammate0))

    return reg_m(list(mat[0][valid_mask]), list(dep_val)).summary(), \
           reg_m(list(mat[0][valid_mask]), [list(mat[1][valid_mask])]).summary(), \
           np.concatenate((mat[0][valid_mask], mat[1][valid_mask], mat[2][valid_mask], mat[3][valid_mask])).reshape(4, len(teammate0))


all_rows = []
for game_type in ["Doubles", "Triples", "Quadruples"]:
    rows = pickle.load(open(game_type + "_table.pkl", "rb"))
    all_rows = all_rows + rows
    # print(game_type, poly(np.array(rows).T, order=int(sys.argv[1]))[1])
    np.save("filtered_" + game_type + ".npy", poly(np.array(rows).T, order=int(sys.argv[1]))[2])
# print("all", poly(np.array(all_rows).T, order=int(sys.argv[1]))[1])
np.save("filtered_all.npy", poly(np.array(all_rows).T, order=int(sys.argv[1]))[2])

