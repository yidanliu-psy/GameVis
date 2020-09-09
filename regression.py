import pickle
import numpy as np
import statsmodels.api as sm
from scipy import stats


# **deprecated**!
# using IQR method to filter away outliers
def outlier(oneD):
    q75, q25 = np.percentile(oneD, [75, 25])
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return np.multiply(oneD < upper, oneD > lower)

# multivariate polyfit
def reg_m(y, x):
    x = x[::-1] # reverse list to make the right output order
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    return sm.RLM(y, X).fit() # using robust linear regression (M-est)


# core code to perform regressions given [delta, I, T, O] matrix
def poly(mat, order=1):
    # 1st order value
    teammate_list = teammate0 = mat[2] / mat[1]
    opponent_list = opponent0 = mat[3] / mat[1]
    i_skill_list = i_skill0 = mat[1]

    interact_list = np.multiply(teammate0, opponent0)

    for i in range(2, order + 1): # add >=1 orders as ind vars for regression
        teammate_list = np.concatenate((teammate_list, np.power(teammate0, i)))
        opponent_list = np.concatenate((opponent_list, np.power(opponent0, i)))
        interact_list = np.concatenate((interact_list, np.multiply(np.power(teammate0, i), np.power(opponent0, i))))
        i_skill_list = np.concatenate((i_skill_list, np.power(i_skill0, i)))

    # I tried following five possible ind var combinations
    # after reshape: [varA^1, varA^2, ..., varA^order, ... , varX^1, varX^2, ..., varX^order]
    I_val = i_skill_list.reshape(order, len(teammate0))
    TvI_val = teammate_list.reshape(order, len(teammate0))
    OvI_val = opponent_list.reshape(order, len(teammate0))
    TvI_OvI_val = np.concatenate((teammate_list, opponent_list)).reshape(order * 2, len(teammate0))
    TvI_OvI_MUL_val = np.concatenate((teammate_list, opponent_list, interact_list)).reshape(order * 3, len(teammate0))

    # do all regressions
    return reg_m(list(mat[0]), list(I_val)), \
           reg_m(list(mat[0]), list(TvI_val)), \
           reg_m(list(mat[0]), list(OvI_val)), \
           reg_m(list(mat[0]), list(TvI_OvI_val)), \
           reg_m(list(mat[0]), list(TvI_OvI_MUL_val))


# inspired by https://github.com/statsmodels/statsmodels/pull/1341
# algorithm: Ch 7 @ Hampel, F. R., Ronchetti, E. M., Rousseeuw, P. J., & Stahel, W. A. (2011). Robust statistics: the approach based on influence functions (Vol. 196). John Wiley & Sons.
def rsquared(result):
    # restore regression paras
    endog = result.model.endog
    mod0 = sm.RLM(endog, np.ones(len(endog)), M=result.model.M)

    # get the fitted output
    res0 = mod0.fit()

    # get rho based on the scale
    rho0 = result.model.M.rho((endog - res0.params) / result.scale).sum()

    return (rho0 - result.model.M.rho(result.sresid).sum()) / rho0


mode_list = ["I", "TvI", "OvI", "TvI_OvI", "TvI_OvI_MUL"]
order_list = [1, 2, 3]
type_list = ["Doubles", "Triples", "Quadruples", "All"]

# read delta table, store all types in a dict
data_dict = {}
all_rows = []
for game_type in type_list[:-1]:
    rows = pickle.load(open(game_type + "_table.pkl", "rb"))
    all_rows = all_rows + rows
    data_dict[game_type] = np.array(rows).T
data_dict[type_list[-1]] = np.array(all_rows).T

# test spearman's rho
for type in type_list:
    mat = data_dict[type]
    delta, I, TvI, OvI = mat[0], mat[1], mat[2] / mat[1], mat[3] / mat[1]
    print(type, stats.spearmanr(delta, I)[0], stats.spearmanr(delta, TvI)[0], stats.spearmanr(delta, OvI)[0])

# regession
# warning: this program *eats* memory!!!
result_file = open("results.txt", "w")
for order in order_list:
    for game_type in type_list:
        poly_results = poly(data_dict[game_type], order=order) # return all five combinations
        for i in range(len(mode_list)):
            print("order:" + str(order), game_type, mode_list[i],
                  rsquared(poly_results[i]), poly_results[i].nobs,
                  "\t".join(map(str, poly_results[i].params)),
                  "\t".join(map(str, poly_results[i].pvalues)),
                  file=result_file) # save results to file
result_file.close()





