# Python Script with functions for the general analytical models used
# Every analytical model has its function with its respective parameters
# The return value is always the calculated effective thermal conductivity

import math as m
import numpy as np

# Parameter description:
# kInlay : thermal conductivity of dispersed filler particle/inlay
# kMatrix : thermal conductivity of the continous surrounding matrix material
# inlayVolFrac : volume/area fraction of inlay and matrix


def maxwell(kInlay, kMatrix, inlayVolFrac):
	kEff = kMatrix * (1 + 3 * inlayVolFrac * 1 / ((kInlay + 2 * kMatrix)/(kInlay - kMatrix) - inlayVolFrac))
	return kEff

def mxwEucken(kInlay, kMatrix, inlayVolFrac):
	numerator = 2 * kMatrix + kInlay - 2 * (kMatrix - kInlay) * inlayVolFrac
	denominator = 2 * kMatrix + kInlay + (kMatrix - kInlay) * inlayVolFrac
	kEff = kMatrix * numerator / denominator
	return kEff

def rayleigh(kInlay, kMatrix, inlayVolFrac):
	raylCorrectionTerm = 1.569 * ((kInlay - kMatrix)/(3 * kInlay - 4 * kMatrix)) * np.power(inlayVolFrac, 10 / 3) 
	kEff = kMatrix * (1 + 3 * inlayVolFrac * 1 / ((kInlay + 2 * kMatrix)/(kInlay - kMatrix) - inlayVolFrac + raylCorrectionTerm))
	return kEff

def rayleighYY(kInlay, kMatrix, inlayVolFrac):
	C1 = (kInlay + kMatrix) / (kInlay - kMatrix)
	C2 = (kInlay - kMatrix) / (kInlay + kMatrix)
	C2Factor = 0.30584 * np.power(inlayVolFrac, 4) + 0.013363 * np.power(inlayVolFrac, 8)
	kEff = kMatrix * (1 + 2 * inlayVolFrac / (C1 - inlayVolFrac + C2 * C2Factor))
	return kEff


# rP : particle inlay radius
# kBound : boundary thermal conductivity between matrix and particle inlay

def sphericalHasselmanJohnson(kInlay, kMatrix, inlayVolFrac, rP, kBound):
	fracIM = kInlay / kMatrix
	fracIrB = kInlay / (rP * kBound)
	numerator = (2 * fracIM - fracIrB - 1) * inlayVolFrac + fracIM + 2 * fracIrB + 2
	denominator = (1 - fracIM + fracIrB) * inlayVolFrac + fracIM + 2 * fracIrB + 2
	kEff= kMatrix * numerator / denominator
	return kEff

def cylindricalHasselmanJohnson(kInlay, kMatrix, inlayVolFrac, rP, kBound):
	fracIM = kInlay / kMatrix
	fracIrB = kInlay / (rP * kBound)
	numerator = (fracIM - fracIrB - 1) * inlayVolFrac + (1 + fracIM + fracIrB)
	denominator = (1 - fracIM + fracIrB) * inlayVolFrac + (1 - fracIM + fracIrB)
	kEff = kMatrix * numerator / denominator
	return kEff

def flatplateHasselmanJohnson(kInlay, kMatrix, inlayVolFrac, rP, kBound):
	fracIM = kInlay / kMatrix
	fracIrB = kInlay / (rP * kBound)
	kEff = kInlay / ((1 - fracIM + 2 * fracIrB) * inlayVolFrac + fracIM)
	return kEff


# alpha : dimensionless parameter depending on ITR between inlay and matrix
# alpha = kapitza radius / radius
# ak : Kapitza radius
# Kapitza radius = interf. therm. res. * kMatrix

def limitingcaseBruggemann(kInlay, kMatrix, inlayVolFrac, rP, rInt):
	ak = rInt * kMatrix
	alpha = ak / rP
	kEff = kMatrix * 1 / (np.power(1 - inlayVolFrac, 3 * (1 - alpha) / (1 + 2 * alpha)))
	return kEff


# Lewis-Nielsen models WIP, they are all implemented for spherical particles

def simplecubicLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.524 # Simple cubic maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / phiM ** 2) * inlayVolFrac
	kEff = kMatrix * (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff

def randomcloseLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.637 # Random close maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / np.power(phiM, 2)) * inlayVolFrac
	kEff = kMatrix * (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff

def randomlooseLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.601 # Random loose maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / np.power(phiM, 2)) * inlayVolFrac
	kEff = kMatrix * (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff


# Higher order analytical model from "Argentinian" paper

def ChiewGland(kInlay, kMatrix, inlayVolFrac):
	fracIM = kInlay / kMatrix
	beta = (fracIM - 1) / (fracIM + 2)
	num = (1 + 2 * beta * inlayVolFrac + (2 * beta ** 3 - 0.1 * beta) * np.power(inlayVolFrac, 2) 
		   + np.power(inlayVolFrac, 3) * 0.05 * m.exp(4.5 * beta))
	denom = 1 - beta * inlayVolFrac
	kEff = kMatrix * num / denom
	return kEff


# Effective phase contrast: Important parameter which tells us the applicability of the
# Maxwell-based models like Maxwell itself or HasselmanJohnson

def effPhaseContrast(kInlay, kMatrix, kEff, rP, rInt):
	gamma = kEff / ((1 + kInlay * rInt / rP) * kMatrix)
	return gamma


# Some meta-function-packages for easier plotting

def funcPack_maxwellbased():
	package = {'Maxwell' : [maxwell, 'k-'], 'Rayleigh' : [rayleigh, 'k:'],
				'RayleighYY' : [rayleighYY, 'k--'], 'Chiew Gland' : [ChiewGland, 'k-.']}
	return package

def funcPack_hasseljohn():
	package = {'Spherical Hasselman Johnson' : [sphericalHasselmanJohnson, 'r-'],
				'Cylindrical Hasselman Johnson' : [cylindricalHasselmanJohnson, 'g-'],
				'Flat-plate Hasselman Johnson' : [flatplateHasselmanJohnson, 'b-']}
	return package

def funcPack_lewisniels():
	package = {'Simple cubic lattice Lewis Nielsen' : [simplecubicLewisNielsen, 'y-'],
				'Random close spherical Lewis Nielsen' : [randomcloseLewisNielsen, 'm-'],
				'Random loose spherical Lewis Nielsen' : [randomlooseLewisNielsen, 'c-']}
	return package

