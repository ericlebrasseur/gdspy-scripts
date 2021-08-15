"""
automatic circular bends for flexible paths
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Path created with automatic bends of radius 5
points = [(0, 0), (0, 10), (20, 0), (18, 15), (8, 15)]
sp4 = gdspy.FlexPath(
    points, 0.5, corners="circular bend", bend_radius=5, gdsii_path=True
)

# Same path, generated with natural corners, for comparison
sp5 = gdspy.FlexPath(points, 0.5, layer=1, gdsii_path=True)

top_cell.add([sp4, sp5])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()