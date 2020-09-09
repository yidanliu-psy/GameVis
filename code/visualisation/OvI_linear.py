# fig. 5
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.3978092294245647, 7.325677230721877, 0.01)  # (min, max, step)
coef_list = [
    [0.4910, -0.4868], # doubles
    [0.3351, -0.3263], # triples
    [0.1721, -0.1673], # quadruples
    [0.3501, -0.3442]  # all
]
# coef for [O/I, constant]

type_list = ["Doubles", "Triples", "Quadruples", "All"]
pattern_list = ['--', '-.', ':', '']

fig, ax = plt.subplots()
for i in range(len(coef_list)):
    y = coef_list[i][0] * x + coef_list[i][1] * 1 # prediction
    ax.plot(x, y, pattern_list[i], label=type_list[i])
ax.set_xlabel('O/I', size=15)
ax.set_ylabel('Δ', size=15)

ax.tick_params(axis='both', direction='in')
plt.yticks(rotation=90)

ax.legend()

plt.savefig("OvI_linear.png", dpi=300)
plt.show()





