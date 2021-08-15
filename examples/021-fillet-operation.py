"""
round polygon corners
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

multi_path = gdspy.Path(2, (-3, -2))
multi_path.segment(4, "+x")
multi_path.turn(2, "l").turn(2, "r")
multi_path.segment(4)

# Create a copy with joined polygons and no fracturing
joined = gdspy.boolean(multi_path, None, "or", max_points=0)
joined.translate(0, -5)

# Fillet applied to each polygon in the path
multi_path.fillet(0.5)

# Fillet applied to the joined copy
joined.fillet(0.5)

top_cell.add([multi_path, joined])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()