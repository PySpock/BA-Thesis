import numpy as np
import matplotlib.pyplot as plt


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
	return key_lines, vals_split


def getData(resultfile, delim='-----'):
	file_lines = readFile(resultfile)
	key_data, val_data = separateKeysVals(file_lines, delim)
	return key_data, val_data


def configPlot(plotloc=2, xOffset=False, yOffset=False):
	ax = plt.gca()
	ax.legend(loc=plotloc)
	ax.get_xaxis().get_major_formatter().set_useOffset(xOffset)
	ax.get_yaxis().get_major_formatter().set_useOffset(yOffset)


# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

ng_vals = [10, 25, 50, 75, 100, 150, 200]

rf_stat = ['stat NG=' + str(ngval) + '.txt' for ngval in ng_vals]
rf_per = ['per NG=' + str(ngval) + '.txt' for ngval in ng_vals]

stat_keys = []
stat_vals = []
per_keys = []
per_vals = []

for datafile_s, datafile_p in zip(rf_stat, rf_per):
	skeys, svals = getData(datafile_s)
	pkeys, pvals = getData(datafile_p)
	stat_keys.append(skeys)
	stat_vals.append(svals)
	per_keys.append(pkeys)
	per_vals.append(pvals)


#print(per_keys[0])
#print(stat_keys[0])
#print(stat_vals[0][0])


# Code, e.g. plotting

itr = [i for i in range(len(stat_vals))]

for i, sv, pv, ngval in zip(itr, stat_vals, per_vals, ng_vals):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	ax.set_ylim(12.00, 12.125)
	ax.set_xlim(-1, 1)
	ax.set_xlabel('Position der Inhomgenität $x$ / m ')
	ax.set_ylabel('Effektive Wärmeleitfähigkeit $\lambda_{\mathrm{eff}}$ in $\mathrm{mW (m \cdot K)^{-1}}$')

	ax.plot(stat_vals[i][2], 1000 * stat_vals[i][0], 'bs', label='$\lambda_{\mathrm{eff}}(x)$ stat. Randbedingung')
	ax.plot(per_vals[i][2], 1000 * per_vals[i][0], 'go', label='$\lambda_{\mathrm{eff}}(x)$ period. Randbedingung')

	configPlot(plotloc=8)

	fig.savefig('N=1_movSphere_per_stat_Comp_ngrid=' + str(ngval) + '.pdf')
	# fig.savefig('N=1 movSphere per_stat Comp ngrid=' + str(ngval) + '.png', dpi=800)
	fig.clear()

"""
ax.set_ylim(0.0105, 0.0111)
ax.set_xlim(-2, 2)
ax.set_xlabel('Abstand Inhomgenitäten $d$ in m ')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')

ax.plot(svals[3], svals[0], 'r+', label='Stat. Randbed.', markersize=8, markeredgewidth=1.25)
ax.plot(pvals[3], pvals[0], 'gx', label='Period. Randbed.', markersize=8, markeredgewidth=1.0)

ax.legend(loc=2)

fig.savefig('N=2 near_coll per_statComp.eps')
fig.savefig('N=2 near_coll per_statComp.pdf')
fig.savefig('N=2 near_coll per_statComp.png', dpi=400)
plt.show()

"""