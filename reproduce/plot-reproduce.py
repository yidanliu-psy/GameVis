# fig. 2
import matplotlib.pyplot as plt
import numpy as np


# results are obtained using `reproduce.py`
x = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]
y = {"Faithfulness": [4.5811, 3.7704, 2.9601, 2.4072, 1.7308, 1.2744, 1.3268, 1.0729, 0.4216, -0.2542, -0.8966, -0.3258, -0.8014, -1.2704],
     "Loyalty": [0.6611, 0.7675, 0.8893, 0.8631, 0.8849, 0.9074, 0.869, 0.9221, 1.0515, 1.0935, 1.2274, 1.0084, 1.0771, 1.2375],
     "TOB": [-1.4717, -1.0837, -0.4751, -0.1631, 0.3025, 0.6281, 0.8281, 1.0814, 1.49, 1.7645, 2.094, 1.9955, 2.0347, 2.2781]}
size_list = [24531, 23365, 16893, 13319, 11021, 9356, 8224, 7324, 6573, 5989, 5488, 4996, 4666, 4350]

pattern_list = ['--', '-.', ':', '']

# plot main results
fig, ax = plt.subplots()
i = 0
for key in y.keys():
    ax.plot(x, y[key], pattern_list[i], label=key)
    i += 1
ax.set_xlabel("Games played", size=15)
ax.set_ylabel("Slope (β)", size=15)

ax.tick_params(axis='both', direction='in')
plt.yticks(rotation=90)

ax.legend()

plt.savefig("reproduce_main.png", dpi=300)
plt.show()

plt.clf()

# plot 'small' fig
fig, ax = plt.subplots()
plt.yscale('log')
ax.plot(x[:2] + x[3:], size_list[:2] + size_list[3:], pattern_list[-1])

ax.set_ylim(1e3, 3e4)

ax.set_xlabel("Games played", size=15)
ax.set_ylabel("Size", size=15)

ax.tick_params(axis='x', direction='in')
plt.yticks(rotation=90)

plt.savefig("reproduce_small.png", dpi=300)
plt.show()




