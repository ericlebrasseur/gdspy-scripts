"""The gdspy.Round class creates circles, ellipses, doughnuts, 
arcs and slices. In all cases, the arguments tolerance or 
number_of_points will control the number of vertices 
used to approximate the curved shapes.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Circle centered at (0, 0), with radius 2 and tolerance 0.01
circle = gdspy.Round((0, 0), 2, tolerance=0.01)
cell.add(circle)

# To create an ellipse, simply pass a list with 2 radii.
# Because the tolerance is small (resulting a large number of
# vertices), the ellipse is fractured in 2 polygons.
ellipse = gdspy.Round((4, 0), [1, 2], tolerance=1e-4)
cell.add(ellipse)

# Circular arc example
arc = gdspy.Round(
    (2, 4),
    2,
    inner_radius=1,
    initial_angle=-0.2 * numpy.pi,
    final_angle=1.2 * numpy.pi,
    tolerance=0.01,
)
cell.add(arc)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
