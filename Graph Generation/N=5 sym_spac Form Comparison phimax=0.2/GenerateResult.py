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

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

resf_Sp = 'SphRes.txt'
resf_Cub = 'CubRes.txt'
resf_Tri = 'TriRes.txt'
resf_Rho = 'RhoRes.txt'
resf_invTri = 'invTriRes.txt'
resf_ElB = 'ElpBRes.txt'
resf_ElH = 'ElpHRes.txt'
delimiter = '-----'

sp_lines = readFile(resf_Sp)
cb_lines = readFile(resf_Cub)
tr_lines = readFile(resf_Tri)
rh_lines = readFile(resf_Rho)
itr_lines = readFile(resf_invTri)
elb_lines = readFile(resf_ElB)
elh_lines = readFile(resf_ElH)
sp_keys, sp_vals = separateKeysVals(sp_lines, delimiter)
cb_keys, cb_vals = separateKeysVals(cb_lines, delimiter)
tr_keys, tr_vals = separateKeysVals(tr_lines, delimiter)
rh_keys, rh_vals = separateKeysVals(rh_lines, delimiter)
itr_keys, itr_vals = separateKeysVals(itr_lines, delimiter)
elb_keys, elb_vals = separateKeysVals(elb_lines, delimiter)
elh_keys, elh_vals = separateKeysVals(elh_lines, delimiter)

# Code, e.g. plotting

print(sp_keys)
print(cb_keys)
print(cb_vals)
print(rh_vals)

vF = np.linspace(0.005, 0.2, 250)
ki = 1.00
km = 0.01
color = ['r-', 'g-', 'y-', 'k-', 'm-', 'b-']
itr = 0


for modelname, model in am.funcPack_maxwellbased().items():
	plt.plot(vF, model(ki, km, vF), color[itr], label=modelname)
	itr += 1
plt.plot(sp_vals[1], sp_vals[0], 'ro', label='Kreisform')
plt.plot(cb_vals[1], cb_vals[0], 'gs', label='Quadratform')
plt.plot(tr_vals[1], tr_vals[0], 'y^', label='Dreieicksform')
plt.plot(itr_vals[1], itr_vals[0], 'mv', label='Dreicksform inv.')
plt.plot(rh_vals[1], rh_vals[0], 'bd', label='Rhombusform')
plt.plot(elb_vals[1], elb_vals[0], 'kp', label='Ellipsenform waager.')
plt.plot(elb_vals[1], elb_vals[0], 'mh', label='Ellipsenform senkr.')
plt.legend(loc=2)
plt.show()