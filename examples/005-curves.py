"""
The class gdspy.Curve can be used to facilitate 
the creation of polygons by drawing their shapes step-by-step. 
It uses a syntax similar to the SVG path specification.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy as np

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Construct a curve made of a sequence of line segments
c1 = gdspy.Curve(0, 0).L(1, 0, 2, 1, 2, 2, 0, 2)
p1 = gdspy.Polygon(c1.get_points())

# Construct another curve using relative coordinates
c2 = gdspy.Curve(3, 1).l(1, 0, 2, 1, 2, 2, 0, 2)
p2 = gdspy.Polygon(c2.get_points())

"""
Coordinate pairs can be given as a complex number: 
real and imaginary parts are used as x and y coordinates, respectively. 
That is useful to define points in polar coordinates.
"""
# Use complex numbers to facilitate writing polar coordinates
c3 = gdspy.Curve(0, 4).l(4 * np.exp(1j * np.pi / 6))
# Elliptical arcs have syntax similar to gdspy.Round
c3.arc((4, 2), 0.5 * np.pi, -0.5 * np.pi)
p3 = gdspy.Polygon(c3.get_points())

cell.add([p1, p2, p3])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
