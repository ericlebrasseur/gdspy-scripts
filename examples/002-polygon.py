""" Create a polygon
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Create a polygon from a list of vertices
points = [(0, 0), (2, 2), (2, 6), (-6, 6), (-6, -6), (-4, -4), (-4, 4), (0, 4)]
poly = gdspy.Polygon(points)
cell.add(poly)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
