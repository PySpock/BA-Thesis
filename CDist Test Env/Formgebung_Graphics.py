import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle, Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)

x_off = 3

cp = [-3 * x_off, 0]
rp = [[x_off, -1], [1 + x_off, 0], [x_off, 1], [-1 + x_off, 0]]
sp = [[-1 - 2* x_off, -1], [1 - 2 * x_off, -1], [1 - 2 * x_off, 1], [-1 - 2 * x_off, 1]]
tup = [[-1 - x_off, -1], [1 - x_off, -1], [-x_off, 1]]
tdo = [[-1 - 0 * x_off, 1], [1 - 0 * x_off, 1], [-0 * x_off, -1]]
el_h = [2 * x_off, 0]
el_v = [3 * x_off, 0]



circle = Circle(cp, 1, fill=True, color='b')
rhombus = Polygon(rp, closed=True, fill=True, color='b')
square = Polygon(sp, closed=True, fill=True, color='b')
triangle_up = Polygon(tup, closed=True, fill=True, color='b')
triangle_down = Polygon(tdo, closed=True, fill=True, color='b')
ellipse_h = Ellipse(el_h, width=2, height=1, angle=0, fill=True, color='b')
ellipse_v = Ellipse(el_v, width=2, height=1, angle=90, fill=True, color='b')

ax.add_patch(circle)
ax.add_patch(rhombus)
ax.add_patch(square)
ax.add_patch(triangle_up)
ax.add_patch(triangle_down)
ax.add_patch(ellipse_h)
ax.add_patch(ellipse_v)

# label poslist

label_pos = [[i * x_off - 0.25, -2.25] for i in range(-3,4)]
labels = ['a)', 'b)', 'c)', 'd)', 'd)', 'e)', 'f)']

for label, labelpos in zip(labels, label_pos):
	ax.annotate(xy=labelpos, s=label)


ax.set_xlim((-11, 11))
ax.set_ylim((-3, 2.5))
ax.set_aspect('equal')

#ax.set_yticklabels([])
#ax.set_xticklabels([])
#ax.set_ticks([])
ax.set_axis_off()

plt.show()
fig.savefig('Formgebung_Graphics.pdf', bbox_inches='tight')


"""

ax.add_patch(Ellipse((4,1.5), 4, 0.5, fill=True, color='b'))
ax.add_patch(Polygon(points, closed=True, fill=True, color='r'))

"""
