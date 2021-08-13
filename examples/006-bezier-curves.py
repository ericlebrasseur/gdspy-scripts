"""
Bezier curves.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy as np

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Cubic Bezier curves can be easily created with C and c
c4 = gdspy.Curve(0, 0).c(1, 0, 1, 1, 2, 1)
# Smooth continuation with S or s
c4.s(1, 1, 0, 1).S(np.exp(1j * np.pi / 6), 0, 0)
p4 = gdspy.Polygon(c4.get_points())

# Similarly for quadratic Bezier curves
c5 = gdspy.Curve(5, 3).Q(3, 2, 3, 0, 5, 0, 4.5, 1).T(5, 3)
p5 = gdspy.Polygon(c5.get_points())

# Smooth interpolating curves can be built using I or i, including
# closed shapes
c6 = gdspy.Curve(0, 3).i([(1, 0), (2, 0), (1, -1)], cycle=True)
p6 = gdspy.Polygon(c6.get_points())

cell.add([p4, p5, p6])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
