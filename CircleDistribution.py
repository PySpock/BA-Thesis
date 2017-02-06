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
	max_attempts = 5000000
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
		last_header_line = content.index('-----\n') + 1

	avg_run_results = np.expand_dims(np.genfromtxt(avg_run_files[0], dtype=np.float64, delimiter=',',
									skip_header=last_header_line, autostrip=True), axis=0)

	for single_runfile in avg_run_files[1:]:
		single_run_arr = np.genfromtxt(single_runfile, dtype=np.float64, delimiter=',',
									   skip_header=last_header_line, autostrip=True)

		avg_run_results = np.concatenate((avg_run_results, 
										  np.expand_dims(single_run_arr, axis=0)), axis=0)

	kMean = np.expand_dims(avg_run_results.mean(axis=0)[0], axis=0)
	kSdev = np.expand_dims(avg_run_results.std(axis=0)[0], axis=0)
	kSerr = kSdev / np.sqrt(len(avg_run_files))
	compiled_results = np.concatenate((kMean, kSdev, kSerr, avg_run_results[1, 1:, :]))

	key_list = ['kMean\n', 'kStDev\n', 'kStdErr\n'] + content[1:last_header_line-1] + ['-----']
	keys = ''.join(key_list)

	np.savetxt('CompiledResult.txt', compiled_results, newline='\n', delimiter=',',
				header=keys, comments='')



def single_simuRun(N_arr, phi, delta=0.01, xL=1.0, yL=0.1):
	flexepath = 'C:\\FlexPDE6\\FlexPDE6n.exe'
	descriptorpath = 'C:\\Users\\Jannik\\Desktop\\Summary\\Rand_Disp phi=0.05 Nmax=50 copy'
	#descriptorpath = 'C:\\Users\\stebanij\\Desktop\\Rand_Disp phi=0.05 Nmax=50 copy'
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
		max_timeouts = 10
		timeouts = 0
		while True:
			try:
				subprocess.call([flexepath, descriptorpath + '\\' + descriptorname], timeout=25)
			except subprocess.TimeoutExpired:
				print(' ')
				print('FlexPDE6n.exe timed out. Retrying current simulation ...')
				print(' ')
				timeouts += 1
				if timeouts >= max_timeouts:
					print('Maximum timeout threshold of ', max_timeouts, ' reached.')
					print('Re-generating current geometry and restarting ...')
					__, raw_pos = generateCircles(N, phi, delta, xL, yL)
					xPos = sortPos(raw_pos)[0]
					yPos = sortPos(raw_pos)[1]
					update[2] = modpars[2] + flexArr(xPos)
					update[3] = modpars[3] + flexArr(yPos)
					updateDescriptor(update, descriptorname)
					timeouts = 0
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

nC = 50
phi = 0.20

#fail_chk, cpos = generateCircles(nC, phi, delta=0.01)
#x = sortPos(cpos)[0]
#y = sortPos(cpos)[1]
#print(sortPos(cpos))

# Plot to control results:

#ctrlPlot(x,y,nC,phi)


# Parameter run:

paramN = np.arange(5, 31, 1)
average_simuRun(paramN, phi, avg_runs=500, delta=0.01)
