import numpy as np
import matplotlib.pyplot as plt
import AnalyticModels as am


volFrac = np.linspace(0.05, 0.7, 250)
ki = 1
km = 0.1

mxw = am.maxwell(ki, km, volFrac)
rayl = am.rayleigh(ki, km, volFrac)
raylYY = am.rayleighYY(ki, km, volFrac)
rcLN = am.randomcloseLewisNielsen(ki, km, volFrac)
rlLN = am.randomlooseLewisNielsen(ki, km, volFrac)

model_results = [mxw, rayl, raylYY, rcLN, rlLN][0:5]
colors = ['r-', 'g-', 'b-', 'y-', 'k-']
labels = ['Maxwell', 'Rayleigh', 'RayleighYY', 'randC LewisN', 'randL LewisN']


for result, color, name in zip(model_results, colors, labels):
	plt.plot(volFrac, result, label = name)

plt.legend(loc=2)
plt.show()