"""
labels are annotations not included in the geometry
texts are polygons included in the geometry
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Label anchored at (1, 3) by its north-west corner
label = gdspy.Label("Sample label", (1, 3), "nw")

# Horizontal text with height 2.25
htext = gdspy.Text("12345", 2.25, (0.25, 6))

# Vertical text with height 1.5
vtext = gdspy.Text("ABC", 1.5, (10.5, 4), horizontal=False)

rect = gdspy.Rectangle((0, 0), (10, 6), layer=10)

top_cell.add([label, htext, vtext, rect])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()