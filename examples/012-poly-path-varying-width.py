"""
Each path component can linearly taper the width of the path 
by using the final_width argument. In the case of a parametric curve, 
more complex width changes can be created by setting final_width to a function.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Start 3 parallel paths with center-to-center distance of 1.5
path3 = gdspy.Path(0.1, (-5.5, 3), number_of_paths=3, distance=1.5)

# Add a segment tapering the widths up to 0.5
path3.segment(2, "-y", final_width=0.5)

# Add a bezier curve decreasing the distance between paths to 0.75
path3.bezier([(0, -2), (1, -3), (3, -3)], final_distance=0.75)

# Add a parametric section to modulate the width with a sinusoidal
# shape.  Note that the algorithm that determines the number of
# evaluations of the parametric curve does not take the width into
# consideration, so we have to manually increase this parameter.
path3.parametric(
    lambda u: (5 * u, 0),
    lambda u: (1, 0),
    final_width=lambda u: 0.4 + 0.1 * numpy.cos(10 * numpy.pi * u),
    number_of_evaluations=256,
)

# Add a circular turn and a final tapering segment.
path3.turn(3, "l")
path3.segment(2, final_width=1, final_distance=1.5)

top_cell.add(path3)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()