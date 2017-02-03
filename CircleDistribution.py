# Brute force generating script for center positions of N circles in a 
# rectangle with the dimensions xLen and yLen. The circles are non-overlapping and 
# have a minimal distance delta to all other objects like boundaries
# or neighbor circles

import numpy as np
import math as m
import random as rnd
import matplotlib.pyplot as plt
import os
import subprocess
import ExtractScript as es

# Set verbosity of console output globally for more info/debugging:
verbose = False
# Be careful with verbosity setting. The console output gets quite big
# for large numbers of particles/inlays/circles

def dist(posA, posB):
	d = m.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)
	return d


def radius(N, phi, xL=1.0, yL=0.1):
	r = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
	return r


def debug(string):
	if verbose:
		print(string)


def testSucc(nC, phi, delta=0.01):
		for i in range(10):
			print('Attempt ', i, ' at generating particles ...')
			generateCircles(nC, phi, delta)


def neighCheck(newpos, rad, ex_circles, delta=0.01):
	neigh_OK = True
	for cpos in ex_circles:
		if dist(newpos,cpos) < 2 * rad + delta:
			neigh_OK = False
			debug('Violation found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
			debug(' ')
			break
		else:
			debug('Accord found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
	return neigh_OK


def generateCircles(N, phi, delta=0.01, xL=1.0, yL=0.1):
	rad = radius(N, phi, xL, yL)
	fail_chk = False
	if rad > yL - delta:
		fail_chk = True
		print(' ')
		print('Error: For N=', N, ' particles and Phi=', phi, 'the radius is bigger than the underlying')
		print('matrix dimension. Could not generate particle position in accordance to conditions!')
		return fail_chk, []
	intervX = xL - rad - delta
	intervY = yL - rad - delta
	ctr = 0
	max_attempts = 25000
	circles = []
	while len(circles) < N:
		newX = rnd.uniform(-intervX,intervX)
		newY = rnd.uniform(-intervY,intervY)
		if neighCheck([newX,newY], rad, circles, delta):
			circles.append([newX,newY])
			debug('Appended!')
			debug(str(circles))
			debug('Length: ' + str(len(circles)))
		ctr = ctr + 1
		if ctr >= max_attempts:
			fail_chk = True
			print(' ')
			print('Warning: Could not finish random circle generation in ' + str(max_attempts) + ' attempts!')
			print('Generated ', len(circles), ' circles of expected N=', N )
			break
	return fail_chk, circles


def sortPos(pos_list):
	xPos = [pos[0] for pos in pos_list]
	yPos = [pos[1] for pos in pos_list]
	return [xPos, yPos]


def ctrlPlot(xPos, yPos, N, phi, xL=1.0, yL=0.1):
	rad = radius(N, phi, xL, yL)
	fig, ax = plt.subplots()
	inlays = []

	for xi, yi in zip(xPos, yPos):
		inlays.append(plt.Circle((xi, yi), rad, color='b', fill=False))
	ax = plt.gca()
	ax.set_xlim((-xL, xL))
	ax.set_ylim((-yL, yL))

	for inlay in inlays:
		ax.add_artist(inlay)
	plt.gca().set_aspect('equal')
	plt.show()


# Special functions for simulating a parameter study with an increasing
# number of particles while the volume fraction is being held constant

def updateDescriptor(update_lines, filename, sep=['{Modifikation Beginn}','{Modifikation Ende}']):
	# Open file in read-mode and update content in-place in memory
	try:
		file = open(filename, 'r')
	except (IOError, FileNotFoundError):
		print('Fatal Error while opening ' + filename + ' Could not complete action.')
		return
	else:
		raw_lines = list(file)
		desc_lines = [line.strip() for line in raw_lines]
		l_index = desc_lines.index(sep[0]) + 1
		h_index = desc_lines.index(sep[1])
		del desc_lines[l_index:h_index]
		for newline in reversed(update_lines):
			desc_lines.insert(l_index, newline)
		file.close()

	# Open file in write mode to overwrite with updated content from memory
	try:
		file = open(filename, 'w')
	except IOError:
		print('Fatal Error while writing ' + filename + ' Could not complete action.')
		return
	else:
		for line in desc_lines:
			file.write(line + '\n')
		file.close()


def flexArr(vals):
	# This function converts a Python list to a flexPDE-styled
	# array of the form array(val1, val2, ..., valN)
	f_array = 'array(' + ','.join([str(val) for val in vals]) + ')'
	return f_array


def compileAvgResults(startString='Avg_Res'):
	# This function collects the data from every average/meta-simulation run and collects
	# it into one file. Standard deviation and error are calculated for the mean heat conduct.

	avg_run_files = es.getFiles(startString)
	with open(avg_run_files[0], 'r') as canary_file:
		content = list(canary_file)
		print(content)
		last_header_line = content.index('-----\n') + 1

	avg_run_results = np.genfromtxt(single_runfile[1], dtype=np.float64, delimiter=',',
										skip_header=last_header_line, autostrip=True)

	for single_runfile in avg_run_files[1:]:
		single_run_arr = np.genfromtxt(single_runfile, dtype=np.float64, delimiter=',',
										skip_header=last_header_line, autostrip=True)
		print(single_run_arr)
		avg_run_results = np.concatenate((avg_run_results, single_run_arr), axis=0)



	"""
	avg_result_files = es.getFiles(startString)
	avg_runs = len(avg_result_files)
	avg_results = []
	keys = []
	for filename in avg_result_files:
		# Open average_res file and seperate it into keys and vals
		# no try-block since getFiles assures existence of files
		curr_file = open(filename, 'r')
		lines_raw = list(curr_file)
		lines = [line.strip() for line in lines_raw]
		split_index = lines.index('-----')
		keys = lines[:split_index]
		vals_str = lines[split_index + 1:]
		vals = [entry.split(',') for entry in vals_str]
		float_vals = [[float(str_val) for str_val in sublist] for sublist in vals]
		avg_results.append(float_vals)
		print(filename)
		print(avg_results)
	# 3D array with index scheme: axis0 -> report parameter/key | axis1 -> stagerun
	# axis2 -> averaging run
	result_array = np.stack(tuple(avg_results), axis=2)
	kMean = np.expand_dims(result_array.mean(axis=2)[0], axis=0)
	kSdev = np.expand_dims(result_array.std(axis=2)[0], axis=0)
	kSerr = np.expand_dims(kSdev / np.sqrt(avg_runs), axis=0)
	print('resarr  ', result_array)
	print('kmean', kMean)
	avg_compilated_arr = np.concatenate((kMean, kSdev, kSerr, result_array[:, :, 0]))
	additional_keys = ['Standard error', 'Standard deviation', 'Mean heat cond. of avg. runs']
	cache = list(reversed(keys))
	keys = list(reversed(cache + additional_keys))
	keys = [''.join([str_item, '\n']) for str_item in keys]
	np.savetxt('AverageEndresult.txt', avg_compilated_arr, delimiter=',', header=keys)
	"""


def single_simuRun(N_arr, phi, delta=0.01, xL=1.0, yL=0.1):
	flexepath = 'C:\\FlexPDE6\\FlexPDE6n.exe'
	#descriptorpath = 'C:\\Users\\Jannik\\Desktop\\Random WIP\\Rand_Disp WIP'
	descriptorpath = 'C:\\Users\\stebanij\\Desktop\\Rand_Disp phi=0.05 Nmax=50 copy'
	descriptorname = 'Rand_Disp Sphere.pde'
	try:
		os.chdir(descriptorpath)
	except OSError:
		print('Error: Could not change directory to ' + descriptorpath)
		print('Aborting simulation run.')
		return

	stagenum = 0
	modpars = ['stagenum = ','number = ','xOff = ','yOff = ','volFrac=']
	update = [0 for param in modpars]
	
	for N in N_arr:
		fail_flag, raw_pos = generateCircles(N, phi, delta, xL, yL)
		stagenum = stagenum + 1
		if fail_flag:
			print('Skipping simulation run ', stagenum, ' due to error during particle generation.')
			print('Possible error #1: Particle radius bigger than matrix dimension')
			print('Possible error #2: Failed to find valid positions for ', N, ' particles')
			continue
		xPos = sortPos(raw_pos)[0]
		yPos = sortPos(raw_pos)[1]
		# Generate list of lines which are updated
		update[0] = modpars[0] + str(stagenum)
		update[1] = modpars[1] + str(int(N))
		update[2] = modpars[2] + flexArr(xPos)
		update[3] = modpars[3] + flexArr(yPos)
		update[4] = modpars[4] + str(phi)
		# Update the descriptor file
		updateDescriptor(update, descriptorname)
		# Run simulation for current iteration in flexPDE
		print('Doing stage run ', stagenum, ' Simulating ', N, 'particles/inlays.')
		while True:
			try:
				subprocess.call([flexepath, descriptorpath + '\\' + descriptorname], timeout=20)
			except subprocess.TimeoutExpired:
				print(' ')
				print('FlexPDE6n.exe timed out. Retrying current simulation ...')
				print(' ')
				continue
			else:
				break
		print(' ')
	print('Finished simulation run!')


def average_simuRun(N_arr, phi, avg_runs, delta=0.01, xL=1.0, yL=0.1):
	for itr in range(1, avg_runs + 1):
		print(' ')
		print('##########################################')
		print('Conducting averaging run', itr, ' of ', avg_runs)
		print('##########################################')
		print(' ')
		single_simuRun(N_arr, phi, delta, xL, yL)
		es.compileResults('Avg_Res_' + str(itr))
	compileAvgResults()



# Set simulation parameters # spheres = nC and volume fraction = phi

nC = 1
phi = 0.05

fail_chk, cpos = generateCircles(nC, phi)
x = sortPos(cpos)[0]
y = sortPos(cpos)[1]
#print(sortPos(cpos))

# Plot to control results:

#ctrlPlot(x,y,nC,phi)

# Test run loop to check the success rate of the circle generation
# with the specified parameters:

#testSucc(nC, phi)

# Parameter run:

paramN = np.arange(1, 4, 1)
average_simuRun(paramN, phi, 2)
