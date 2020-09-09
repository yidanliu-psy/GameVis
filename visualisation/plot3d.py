# fig. 6
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

# (min, max, step)
TvI = np.arange(0.15325244251267134, 6.525181482293945, 0.1)
OvI = np.arange(0.3978092294245647, 7.325677230721877, 0.1)
TvI, OvI = np.meshgrid(TvI, OvI)

# prediction
delta = -0.07638066587989004 * TvI + 0.36871771354839195 * OvI -0.2864272032225875

# plot the surface.
surf = ax.plot_surface(TvI, OvI, delta, cmap=cm.cividis_r, linewidth=0, antialiased=False)

ax.set_zlim(-1.0, 2.7)
ax.set_zticks(np.arange(-1.0, 2.6, 0.5))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.01f'))
ax.set_zlabel('Δ', size=20)
ax.set_ylabel('  O/I  ', size=20)
ax.set_xlabel('  T/I  ', size=20) 
# *trick: I find that the text will only become parallel to the axis when it's long enough...

# add a color bar
cb = fig.colorbar(surf, shrink=0.5, aspect=5)

# change tick color to distinguish from label
plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='blue')
ax.tick_params(axis='x', colors='blue', length=0)
ax.tick_params(axis='y', colors='blue', length=0)
ax.tick_params(axis='z', colors='blue', length=0)

plt.savefig("TvI_OvI.png", dpi=300)
plt.show()
