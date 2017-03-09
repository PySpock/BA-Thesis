import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import itertools


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

def extract_from_flextbl(filename, separators=['X', 'Y', 'DATA']):
	with open(filename, 'r') as ftb:
		lines_raw = list(ftb)
	# Cleanup header and newlines
	lines = [rawline.strip() for rawline in lines_raw]
	h_end = lines.index('}') + 1
	lines = lines[h_end:]
	lines = [line for line in lines if line != '']
	# Split data on separators
	sep_indexes = []
	data_points = 0
	for index, line in enumerate(lines):
		for separator in separators:
			if line[0:len(separator)] == separator:
				sep_indexes.append(index)
				if separator == 'X':
					data_points = int(line[1:].strip())

	x = lines[sep_indexes[0] + 1:sep_indexes[1]]
	y = lines[sep_indexes[1] + 1:sep_indexes[2]]
	data = lines[sep_indexes[2] + 1:]

	data_list = [x, y, data]
	data_list = [[item.split() for item in sublist] for sublist in data_list]
	# Flatten the sublists
	data_list = [list(itertools.chain.from_iterable(sublist)) for sublist in data_list]
	# Convert to float for plotting
	data_list = [[float(item) for item in sublist] for sublist in data_list]

	z = [[data_list[2][i] for i in range(j*data_points, (j+1)*data_points)] for j in range(0, data_points)]
	data_list[2] = np.asarray(z)

	return data_list


os.chdir(r'C:\Users\stebanij\Desktop\N=5 sym_spaced Spheres - Kopie')

file = '5_Sphere_varVolFrac_01.tbl'

data = extract_from_flextbl(file)
x = data[0]
y = data[1]
z = data[2]


xc, yc = np.meshgrid(x, y, indexing=('xy'))

"""
print('XXX:', len(xc[0]))
print('YYY: ', yc[0:2])
print('TEMP:', z[0], '51^2=', 51**2)

print('Shape xc:', xc.shape)
print('Shape yc:', yc.shape)
print('Shape z:', z.shape)

k = 25

print('XXX: ', xc[k])
print('YYY: ', yc[k])
print('ZZZ: ', z[k])
"""

cont = np.linspace(10, 50, 30)

fig = plt.figure()
ax = fig.add_subplot(111)

rstride = 1
cstride = 1

ax.set_xlabel('X')
ax.set_ylabel('Y')
#ax.set_zlabel('TEMP')
ax.set_aspect('equal')

ax.contour(xc, yc, z, levels=cont)


plt.show()


"""

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rstride = 1
cstride = 1

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('TEMP')

ax.plot_wireframe(xc, yc, z, rstride=rstride, cstride=cstride)

plt.show()
"""