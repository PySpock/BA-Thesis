import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

"""
x = np.linspace(-4, 4, 50)
y = np.linspace(-4, 4, 50)

xc, yc = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rstride = 10
cstride = 10

ax.plot_wireframe(xc, yc, np.sin(xc+yc), rstride=rstride, cstride=cstride)

plt.show()
"""

os.chdir(r'C:\Users\stebanij\Desktop\N=5 sym_spaced Spheres - Kopie')
print(os.getcwd())

with open('5_Sphere_varVolFrac_01.tbl', 'r') as ftb:
	lines = list(ftb)
	print(lines[0:50])