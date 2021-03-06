import numpy as np
import matplotlib.pyplot as plt
import math as m

def radius(N, phi, xL=1.0, yL=0.1):
	r = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
	return r

def dist(pointA, pointB):
	# Euclidean norm in arbitrary dimension < inf
	dsquared = 0
	for coordA, coordB in zip(pointA, pointB):
		dsquared += (coordA - coordB) ** 2
	return m.sqrt(dsquared)


def sinusoid_Mov(phi, plot_points, periodes=1, delta=0.01, xL=1.0, yL=0.1):
	# Sanity check of sphere size
	r = radius(1, phi, xL, yL)
	print(r)
	if yL - r < delta:
		print('Error: Sphere with volume fraction ', phi, ' exceeds the underlying mesh size.')
		print('Aborting position generation')
		return (0, 0)
	elif r - yL < -0.5 * r:
		print('Warning: With the specified parameters the wiggle room for the sphere')
		print('is less than 5/10 of the radius.')

	# Particle edges should stay within minimum distance delta to mesh boundaries
	amplitude = yL - r - delta
	boundary = xL - r - delta
	xPos = np.linspace(-boundary, boundary, plot_points)
	yPos = amplitude * np.sin((periodes * np.pi) / boundary * xPos)
	positions = [xPos, yPos]
	return positions

def nearmiss_Spheres(phi, plot_points, delta=0.01, refine=False, lo=-0.3, hi=0.3, ref_points=75, xL=1.0, yL=0.1):
	# Pre-conducted sanity check whether the spheres fit into the underlying
	# mesh with the specified parameters
	r = radius(2, phi, xL, yL)
	print(r)
	if 2 * r + 3 * delta > yL:
		print('Error: Current parameters and safety distances imply a mesh collision')
		print('Aborting position generation!')
		return (0, 0, 0, 0)
	boundary = xL - r - delta
	if refine:
		xPosL = np.linspace(-boundary, lo, plot_points // 2, endpoint=False)
		xPosL = np.append(xPosL, np.linspace(lo, hi, ref_points, endpoint=False))
		xPosL = np.append(xPosL, np.linspace(hi, boundary, plot_points // 2))
	else:
		xPosL = np.linspace(-boundary, boundary, plot_points)
	xPosR = -xPosL
	yPosL = -yL + r + delta 
	yPosR = yPosL
	positions = [xPosL,yPosL,xPosR,yPosR]
	return positions


pos_sin = sinusoid_Mov(0.005, 75, 1)
#pos = nearmiss_Spheres(0.025, 50, 0.0065, True)
#print(pos)
print(pos_sin)

#plt.plot(x, y)
#plt.show()