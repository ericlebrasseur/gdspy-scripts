"""
The class gdspy.Path is designed to allow the creation of 
path-like polygons in a piece-wise manner.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Start a path at (0, 0) with width 1
path1 = gdspy.Path(1, (0, 0))

# Add a segment to the path goin in the '+y' direction
path1.segment(4, "+y")

# Further segments or turns will folow the current path direction
# to ensure continuity
path1.turn(2, "r")
path1.segment(1)
path1.turn(3, "rr")

top_cell.add(path1)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()