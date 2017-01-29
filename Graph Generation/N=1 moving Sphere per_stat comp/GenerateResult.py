import os
import numpy as np
import matplotlib.pyplot as plt
import AnalyticModels as am

def readFile(name):
	try:
		file = open(name, 'r')
	except IOError:
		print('File ' + name + ' not found or inaccessible')
		line_list = []
		pass
	else:
		line_list_raw = list(file)
		file.close()
		line_list = [line.strip() for line in line_list_raw]
	return line_list

def separateKeysVals(line_list, delimiter):
	try:
		split_index = line_list.index(delimiter)
	except ValueError:
		return ('Empty', 'Empty')
	else:
		key_lines = line_list[:split_index]
		val_lines = line_list[split_index + 1:]
		vals_split = np.asarray([line.split(',') for line in val_lines], dtype=np.float64)
		# Implementation with "classic" Python lists
		#val_lines_clean = []
		#for stritem in val_lines:
		#	cache = stritem.split(',')
		#	val_lines_clean.append([float(value) for value in cache])
	return key_lines, vals_split


def getData(resultfile, delim='-----'):
	file_lines = readFile(resultfile)
	key_data, val_data = separateKeysVals(file_lines, delim)
	return key_data, val_data

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

per_res = 'PerRes.txt'
stat_res = 'StatRes.txt'

pkeys, pvals = getData(per_res)
skeys, svals = getData(stat_res)

# Code, e.g. plotting

print(pkeys)
print(pvals)
print(svals)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set_xlim(0.008, 0.385)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Position der Inhomogenität $x$ in m')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')


ax.plot(svals[2], 1000*svals[0], 'ro', label='Feste Randbedingung')
ax.plot(pvals[2], 1000*pvals[0], 'g^', label='Periodische Randbedingung')


ax.legend(loc=8)

fig.savefig('Per_Stat Comp moving Sphere.eps')
fig.savefig('Per_Stat Comp moving Sphere.pdf')
fig.savefig('Per_Stat Comp moving Sphere', dpi=800)
plt.show()
