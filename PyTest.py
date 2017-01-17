import numpy as np
import matplotlib.pyplot as plt
import math
import AnalyticModels as am

def f(t):
	return np.exp(- 0.5*t) * np.sin(5 * t)

volFrac = np.linspace(0, 0.75, 25)

maxwellData = am.maxwell(10, 0.1, volFrac)
rayleighData = am.rayleigh(10, 0.1, volFrac)
raylYYData = am.rayleighYY(10, 0.1, volFrac)

plt.plot(volFrac, maxwellData, 'bs', label = 'Maxwell model')
plt.plot(volFrac, rayleighData, 'ro', label = 'Rayleigh model')
plt.plot(volFrac, raylYYData, 'g^', label = 'Rayleigh YY model')
plt.legend(loc = 'upper left')
plt.xlabel('Volume Fraction')
plt.ylabel('Effective thermal conductivity')
plt.show()

#plt.plot(x1, f(x1), 'bs', x2, f(x2), 'k')
#plt.plot(x2, np.exp(-0.5*x2), 'r-', x2, -np.exp(-0.5*x2), 'r-')
#plt.ylim(-1, 1)
#plt.xlabel('test')
# plt.show()

#plt.savefig('test.pdf')