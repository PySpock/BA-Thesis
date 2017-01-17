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

def rayleigh(kInlay, kMatrix, inlayVolFrac):
	raylCorrectionTerm = 1.569 * ((kInlay - kMatrix)/(3 * kInlay - 4 * kMatrix)) * np.power(inlayVolFrac, 10 / 3) 
	kEff = kMatrix * (1 + 3 * inlayVolFrac * 1 / ((kInlay + 2 * kMatrix)/(kInlay - kMatrix) - inlayVolFrac + raylCorrectionTerm))
	return kEff

def rayleighYY(kInlay, kMatrix, inlayVolFrac):
	C1 = (kInlay + kMatrix) / (kInlay - kMatrix)
	C2 = (kInlay - kMatrix) / (kInlay + kMatrix)
	c2Factor = 0.30584 * np.power(inlayVolFrac, 4) + 0.013363 * np.power(inlayVolFrac, 8)
	kEff = kMatrix * (1 + 2 * inlayVolFrac / (C1 - inlayVolFrac + C2 * c2Factor))
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
# ak : Kapitza radius

def limitingcaseBruggemann(kInlay, kMatrix, inlayVolFrac, rP, rInt):
	ak = rInt * kMatrix
	alpha = ak / rP
	kEff = kMatrix * 1 / (np.power(1 - inlayVolFrac, 3 * (1 - alpha) / (1 + 2 * alpha)))
	return kEff

def simplecubicLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.524 # Simple cubic maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / phiM ** 2) * inlayVolFrac
	kEff = (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff

def randomcloseLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.637 # Random close maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / np.power(phiM, 2)) * inlayVolFrac
	kEff = (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff

def randomlooseLewisNielsen(kInlay, kMatrix, inlayVolFrac):
	shapePar = 1.5 # Shape Parameter of inlay (here spherical) as required by model
	phiM = 0.601 # Random loose maximum packaging fraction 
	b = (kInlay / kMatrix - 1) / (kInlay / kMatrix + shapePar)
	psi = 1 + ((1 - phiM) / np.power(phiM, 2)) * inlayVolFrac
	kEff = (1 + shapePar * b * inlayVolFrac) / (1 - b * psi * inlayVolFrac)
	return kEff


# Effective phase contrast: Important parameter which tells us the applicability of the
# Maxwell-based models like Maxwell or HasselmanJohnson

def effPhaseContrast(kInlay, kMatrix, kEff, rP, rInt):
	gamma = kEff / ((1 + kInlay * rInt / a) * kMatrix)
	return gamma

print(maxwell(10,0.01,0.2))
print(rayleigh(10, 0.01,0.2))
