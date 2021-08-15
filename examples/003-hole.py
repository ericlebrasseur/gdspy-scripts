""" Create a hole (or cutout)
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Manually connect the hole to the outer boundary
cutout = gdspy.Polygon(
    [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0), (2, 2), (2, 3), (3, 3), (3, 2), (2, 2)])

cell.add(cutout)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
