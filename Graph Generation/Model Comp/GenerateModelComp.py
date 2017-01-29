import os
import numpy as np
import matplotlib.pyplot as plt
import AnalyticModels as am

vF = np.linspace(0.005, 0.5, 350)
ki = 1.0
km = 0.01

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set_xlim(0.008, 0.385)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Volume fraction $\phi$')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')

for mwkey, mwmodparam in am.funcPack_maxwellbased().items():
	ax.plot(vF, mwmodparam[0](ki,km,vF), mwmodparam[1], label=mwkey)

for lnkey, lnmodparam in am.funcPack_lewisniels().items():
	ax.plot(vF, lnmodparam[0](ki,km,vF), lnmodparam[1], label=lnkey)


ax.legend(loc=2)


fig.savefig('Model Comp.pdf')
fig.savefig('Model Comp.png', dpi=800)
plt.show()