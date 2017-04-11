"""
Template script to pull data from standardized
flexPDE TABLE() output. Thereafter, plotting is
easily done
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import itertools


def extract_from_flextbl(filename, separators=['X', 'Y', 'DATA']):
	""" Open a flexPDE generated TABLE-file and extract the data fields X, Y
		and DATA from it in a structured manner"""
	with open(filename, 'r') as ftb:
		lines_raw = list(ftb)
	# Cleanup header and newlines
	lines = [rawline.strip() for rawline in lines_raw]
	h_end = lines.index('}') + 1
	lines = lines[h_end:]
	lines = [line for line in lines if line != '']
	# Split data on separators
	sep_indexes = []
	for index, line in enumerate(lines):
		for separator in separators:
			if line[0:len(separator)] == separator:
				sep_indexes.append(index)

	x = lines[sep_indexes[0] + 1:sep_indexes[1]]
	y = lines[sep_indexes[1] + 1:sep_indexes[2]]
	data = lines[sep_indexes[2] + 1:]

	# Repackage data and split separate values
	data_list = [x, y, data]
	data_list = [[item.split() for item in sublist] for sublist in data_list]
	# Flatten the sublists
	data_list = [list(itertools.chain.from_iterable(sublist)) for sublist in data_list]
	# Convert to float for plotting
	data_list = [[float(item) for item in sublist] for sublist in data_list]
	# Get number of data points on axis
	data_points = len(data_list[0])

	# Split z-data so that a sublist corresponds to a row of discrete points
	z = [[data_list[2][i] for i in range(j*data_points, (j+1)*data_points)] for j in range(0, data_points)]
	data_list[2] = np.asarray(z)

	return data_list


def plot_tempfield(data_list):
	""" Basic plot function to quickly shell out a countourf() plot
		of the temperature field. For customized plotting resort to
		manually configured plots or configure this function body"""
	x = data_list[0]
	y = data_list[1]
	zc = data_list[2]
	xc, yc = np.meshgrid(x, y)
	cont = np.linspace(10, 50, 400)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.set_xlabel('X')
	ax.set_ylabel('Y', rotation='horizontal')
	ax.set_yticks([-0.1, 0, 0.1])
	ax.set_aspect(aspect=1)

	ctf = ax.contourf(xc, yc, zc, levels=cont)

	divider = make_axes_locatable(ax)
	cax  = divider.append_axes('top', size='10%', pad=0.3)

	# fix wierd antialiasing thingy
	for c in ctf.collections:
		c.set_edgecolor('face')

	cbar = plt.colorbar(ctf, cax=cax, orientation='horizontal')
	cbar.ax.xaxis.set_ticks_position('top')
	cbar.ax.set_ylabel('Temp', labelpad=30, rotation='horizontal')
	cbar_ticks = np.arange(10, 60, 5)
	cbar.set_ticks(cbar_ticks)

	plt.show()

filename = 'N=5 symm_spaced Ellipses high_01.tbl'

data = extract_from_flextbl(filename)
plot_tempfield(data)