"""
expands or contracts polygons by a fixed amount
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

rect1 = gdspy.Rectangle((-4, -4), (1, 1))
rect2 = gdspy.Rectangle((-1, -1), (4, 4))

# Offset both polygons
# Because we join them first, a single polygon is created.
outer = gdspy.offset([rect1, rect2], 0.5, join_first=True, layer=1)

top_cell.add([rect1, rect2, outer])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()