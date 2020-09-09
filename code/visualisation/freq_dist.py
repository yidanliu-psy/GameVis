# plot data distribution (fig. 3)
import numpy as np
import matplotlib.pyplot as plt

data = np.load('all.npy') # `all.npy` is the concatenation of tables of three types

var_list = ['Δ', 'I', 'OvI', 'TvI']

for i in range(4):
    plt.clf()
    plt.hist(data[i], 5000, normed=True, alpha=0.75)
    plt.xlabel(var_list[i], size=15)
    plt.ylabel('Frequency density', size=15)
    plt.grid(True)

    plt.savefig(var_list[i] + "_dist.png", dpi=300)
    plt.show()