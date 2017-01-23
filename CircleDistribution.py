# Generating script for center positions of N circles in a rectangle with
# the dimensions xLen and yLen. The circles are non-overlapping and 
# have a minimal distance delta to all other objects like boundaries
# or neighbor circles

import numpy as np
import math as m
import random as rnd
import matplotlib.pyplot as plt
import logging

# Set verbosity of console output globally for info/debugging:

verbose = True

def dist(posA, posB):
	d = m.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)
	return d

def debug(string):
	if verbose:
		print(string)
	return None

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
	rad = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
	print(rad)
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
			print('Generated ' + len(circles) + ' circles of expected N=' + str(N))
			break
	return circles

def sortPos(pos_list):
	xPos = [pos[0] for pos in pos_list]
	yPos = [pos[1] for pos in pos_list]
	return [xPos, yPos]

def ctrlPlot(xPos, yPos, N, phi, xL=1.0, yL=0.1):
	rad = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
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
	return None


# Set simulation parameters # spheres = nC and volume fraction = phi

nC = 10
phi = 0.2

cpos = generateCircles(nC, phi)
x = sortPos(cpos)[0]
y = sortPos(cpos)[1]
print(sortPos(cpos))

#Plot to control results:

ctrlPlot(x,y,nC,phi)

