"""
use robust paths when flexible paths fail
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Create 4 parallel paths in different layers
lp = gdspy.RobustPath(
    (50, 0),
    [2, 0.5, 1, 1],
    [0, 0, -1, 1],
    ends=["extended", "round", "flush", "flush"],
    layer=[0, 2, 1, 1],
)
lp.segment((45, 0))
lp.segment(
    (5, 0),
    width=[lambda u: 2 + 16 * u * (1 - u), 0.5, 1, 1],
    offset=[
        0,
        lambda u: 8 * u * (1 - u) * numpy.cos(12 * numpy.pi * u),
        lambda u: -1 - 8 * u * (1 - u),
        lambda u: 1 + 8 * u * (1 - u),
    ],
)
lp.segment((0, 0))
lp.smooth(
    [(5, 10)],
    angles=[0.5 * numpy.pi, 0],
    width=0.5,
    offset=[-0.25, 0.25, -0.75, 0.75],
)
lp.parametric(
    lambda u: numpy.array((45 * u, 4 * numpy.sin(6 * numpy.pi * u))),
    offset=[
        lambda u: -0.25 * numpy.cos(24 * numpy.pi * u),
        lambda u: 0.25 * numpy.cos(24 * numpy.pi * u),
        -0.75,
        0.75,
    ],
)

top_cell.add(lp)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()