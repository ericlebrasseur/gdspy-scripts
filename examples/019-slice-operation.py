"""
a slice operation subdivides a set of polygons along horizontal or vertical cut lines
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

ring1 = gdspy.Round((-6, 0), 6, inner_radius=4)
ring2 = gdspy.Round((0, 0), 6, inner_radius=4)
ring3 = gdspy.Round((6, 0), 6, inner_radius=4)

# Slice the first ring across x=-3, the second ring across x=-3
# and x=3, and the third ring across x=3
slices1 = gdspy.slice(ring1, -3, axis=0)
slices2 = gdspy.slice(ring2, [-3, 3], axis=0)
slices3 = gdspy.slice(ring3, 3, axis=0)

slices = gdspy.Cell("SLICES")

# Keep only the left side of slices1, the center part of slices2
# and the right side of slices3
slices.add(slices1[0])
slices.add(slices2[1])
slices.add(slices3[1])

top_cell.add(slices)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()