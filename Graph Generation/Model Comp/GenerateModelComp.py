import os
import numpy as np
import matplotlib.pyplot as plt
import AnalyticModels as am

vF = np.linspace(0.0, 0.2, 1000)
ki = 1.0
km = 0.01

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set_xlim(0.008, 0.385)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Volumenanteil $\phi$ / 1')
ax.set_ylabel('Effektive Wärmeleitfähigkeit $\lambda_{\mathrm{eff}}$ / $\mathrm{W (m \cdot K)^{-1}}$')

for mwkey, mwmodparam in am.funcPack_maxwellbased().items():
	if True: #mwkey != 'Chiew Gland':
		ax.plot(vF, mwmodparam[0](ki,km,vF), mwmodparam[1], label=mwkey)

for lnkey, lnmodparam in am.funcPack_lewisniels().items():
	ax.plot(vF, lnmodparam[0](ki,km,vF), lnmodparam[1], label=lnkey)


ax.legend(loc=2, fontsize=12)


fig.savefig('Model_Comp_0-0.2.pdf')
#fig.savefig('Model_Comp.png', dpi=800)
plt.show()

vF = np.linspace(0.2, 0.5, 1000)
ki = 1.0
km = 0.01

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set_xlim(0.008, 0.385)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Volumenanteil $\phi$ / 1')
ax.set_ylabel('Effektive Wärmeleitfähigkeit $\lambda_{\mathrm{eff}}$ / $\mathrm{W (m \cdot K)^{-1}}$')

for mwkey, mwmodparam in am.funcPack_maxwellbased().items():
	if True: #mwkey != 'Chiew Gland':
		ax.plot(vF, mwmodparam[0](ki,km,vF), mwmodparam[1], label=mwkey)

for lnkey, lnmodparam in am.funcPack_lewisniels().items():
	ax.plot(vF, lnmodparam[0](ki,km,vF), lnmodparam[1], label=lnkey)


ax.legend(loc=2, fontsize=14)


fig.savefig('Model_Comp_0.2-0.5.pdf')
#fig.savefig('Model_Comp.png', dpi=800)
plt.show()