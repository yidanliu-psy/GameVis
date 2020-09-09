# plot 2d 2rd-order regression 
import matplotlib.pyplot as plt
import numpy as np

I = np.arange(4.40990640657, 58.51715740979401, 0.1) # (min, max, step)
I_coef_list = [
    [-0.13927776461608068, 0.002038919337462459, 2.3484253283211487], # doubles
    [-0.09850865867608666, 0.001429693439506745, 1.673346834786426], # triples
    [-0.04062711141502941, 0.0005561811330575912, 0.7243531132252763], # quadruples
    [-0.09931019535824288, 0.0014388069537618795, 1.6896976115572775] # all
]
# coef for [order-1, order-2, constant]

OvI = np.arange(0.3978092294245647, 7.325677230721877, 0.01)
OvI_coef_list = [
    [0.08149445158061253, 0.19664308140877118, -0.27567136158525557],
    [0.1691745820752472, 0.07835210254462913, -0.23984672383683908],
    [0.055910443720261264, 0.05469892798492301, -0.10648949308046807],
    [0.15332557744227973, 0.09344338104295906, -0.24194502634113763]
]


# now set for fig. 4
x = I
coef_list = I_coef_list
name = "I"

type_list = ["Doubles", "Triples", "Quadruples", "All"]
pattern_list = ['--', '-.', ':', '']

fig, ax = plt.subplots()
for i in range(len(coef_list)):
    y = coef_list[i][0] * x + coef_list[i][1] * np.power(x, 2) + coef_list[i][2] * 1 # prediction
    ax.plot(x, y, pattern_list[i], label=type_list[i])
ax.set_xlabel(name, size=15)
ax.set_ylabel('Δ', size=15)

ax.tick_params(axis='both', direction='in')
plt.yticks(rotation=90)

ax.legend()

plt.savefig(name.replace('/', 'v') + ".png", dpi=300)
plt.show()





