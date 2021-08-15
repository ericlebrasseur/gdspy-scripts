"""
flexible paths overcome some limitations of polygon paths
for instance, you can define a path by a sequence of points
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Path defined by a sequence of points and stored as a GDSII path
sp1 = gdspy.FlexPath(
    [(0, 0), (3, 0), (3, 2), (5, 3), (3, 4), (0, 4)], 1, gdsii_path=True
)

# Other construction methods can still be used
sp1.smooth([(0, 2), (2, 2), (4, 3), (5, 1)], relative=True)

# Multiple parallel paths separated by 0.5 with different widths,
# end caps, and joins.  Because of the join specification, they
# cannot be stared as GDSII paths, only as polygons.
sp2 = gdspy.FlexPath(
    [(12, 0), (8, 0), (8, 3), (10, 2)],
    [0.3, 0.2, 0.4],
    0.5,
    ends=["extended", "flush", "round"],
    corners=["bevel", "miter", "round"],
)
sp2.arc(2, -0.5 * numpy.pi, 0.5 * numpy.pi)
sp2.arc(1, 0.5 * numpy.pi, 1.5 * numpy.pi)

top_cell.add([sp1, sp2])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()