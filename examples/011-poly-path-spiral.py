"""
More complex paths can be constructed with the methods 
gdspy.Path.bezier(), gdspy.Path.smooth(), and gdspy.Path.parametric()
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

path2 = gdspy.Path(0.5, (0, 0))

# Start the path with a smooth Bezier S-curve
path2.bezier([(0, 5), (5, 5), (5, 10)])

# We want to add a spiral curve to the path.  The spiral is defined
# as a parametric curve.  We make sure spiral(0) = (0, 0) so that
# the path is continuous.
def spiral(u):
    r = 4 - 3 * u
    theta = 5 * u * numpy.pi
    x = r * numpy.cos(theta) - 4
    y = r * numpy.sin(theta)
    return (x, y)

# It is recommended to also define the derivative of the parametric
# curve, otherwise this derivative must be calculated nummerically.
# The derivative is used to define the side boundaries of the path,
# so, in this case, to ensure continuity with the existing S-curve,
# we make sure the the direction at the start of the spiral is
# pointing exactly upwards, as if is radius were constant.
# Additionally, the exact magnitude of the derivative is not
# important; gdspy only uses its direction.
def dspiral_dt(u):
    theta = 5 * u * numpy.pi
    dx_dt = -numpy.sin(theta)
    dy_dt = numpy.cos(theta)
    return (dx_dt, dy_dt)

# Add the parametric spiral to the path
path2.parametric(spiral, dspiral_dt)

top_cell.add(path2)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()