import pickle
import numpy as np
import statsmodels.api as sm

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

all_rows = []
for game_type in ["Doubles", "Triples", "Quadruples"]:
    rows = pickle.load(open(game_type + "_table.pkl", "rb"))
    all_rows = all_rows + rows
    
    print(game_type, reg_m(list(np.array(rows).T)[0], list(np.array(rows).T)[1:]).summary())
print("all", reg_m(list(np.array(all_rows).T)[0], list(np.array(all_rows).T)[1:]).summary())

# delta = p1*opponent + p2*teammate + p3*self_init + c