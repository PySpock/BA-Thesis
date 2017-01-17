import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def f(x, y):
	return np.exp(- 0.5 * np.abs(x * y))

def expandInterval(array):
	return 'lol'


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



xraw = 5 * np.random.random(250)
yraw = 5 * np.random.random(250)

x = np.append(xraw,-xraw)
y = np.append(yraw,-yraw)

x = np.append(x, xraw)
y = np.append(y, -yraw)

x = np.append(x, -xraw)
y = np.append(y, yraw)





z = f(x, y)

ax.scatter(x, y, z)

ax.set_xlabel('X Achse')
ax.set_ylabel('Y Achse')
ax.set_zlabel('Z Achse')

# print(-x)




plt.show()