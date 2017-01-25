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


def generateCircles(N, phi, xL=1.0, yL=0.1, delta=0.01):
	rad = radius(N, phi, xL, yL)
	intervX = xL - rad - delta
	intervY = yL - rad - delta
	ctr = 0
	max_attempts = 10000
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
			print('Warning: Could not finish random circle generation in ' + str(max_attempts) + ' attempts!')
			print('Generated ', len(circles), ' circles of expected N=', N )
			break
	return circles


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


def simuRun(N_arr, phi, xL=1.0, yL=0.1, delta=0.01):
	flexepath = 'C:\\FlexPDE6\\FlexPDE6n.exe'
	descriptorpath = 'C:\\Users\\Jannik\\Desktop\\Random WIP\\Rand_Disp WIP'
	descriptorname = 'Rand_Disp Sphere.pde'
	try:
		os.chdir(descriptorpath)
	except OSError:
		print('Error: Could not change directory to ' + descriptorpath)
		print('Aborting simulation run.')
		return

	stagenum = 0
	modpars = ['stagenum = ','number = ','xOff = ','yOff = ']
	update = [0 for param in modpars]
	
	for N in N_arr:
		raw_pos = generateCircles(N, phi, xL, yL, delta)
		xPos = sortPos(raw_pos)[0]
		yPos = sortPos(raw_pos)[1]
		stagenum = stagenum + 1
		# Generate list of lines which are updated
		update[0] = modpars[0] + str(stagenum)
		update[1] = modpars[1] + str(int(N))
		update[2] = modpars[2] + flexArr(xPos)
		update[3] = modpars[3] + flexArr(yPos)
		# Update the descriptor file
		updateDescriptor(update, descriptorname)
		# Run simulation for current iteration in flexPDE
		print('Doing stage run ', stagenum, ' Simulating ', N, 'particles/inlays.')
		subprocess.call([flexepath, descriptorpath + '\\' + descriptorname])
	print('Finished simulation run successfully!')



# Set simulation parameters # spheres = nC and volume fraction = phi

nC = 10
phi = 0.2

cpos = generateCircles(nC, phi)
x = sortPos(cpos)[0]
y = sortPos(cpos)[1]
# print(sortPos(cpos))

# Plot to control results:

# ctrlPlot(x,y,nC,phi)

paramN = np.arange(1,101,1)
simuRun(paramN, 0.2)
