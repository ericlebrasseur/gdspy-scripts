"""
flexible paths overcome some limitations of polygon paths
for instance, you can define a path by a sequence of points
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Path corners and end caps can be custom functions.
# This corner function creates 'broken' joins.
def broken(p0, v0, p1, v1, p2, w):
    # Calculate intersection point p between lines defined by
    # p0 + u0 * v0 (for all u0) and p1 + u1 * v1 (for all u1)
    den = v1[1] * v0[0] - v1[0] * v0[1]
    lim = 1e-12 * (v0[0] ** 2 + v0[1] ** 2) * (v1[0] ** 2 + v1[1] ** 2)
    if den ** 2 < lim:
        # Lines are parallel: use mid-point
        u0 = u1 = 0
        p = 0.5 * (p0 + p1)
    else:
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        u0 = (v1[1] * dx - v1[0] * dy) / den
        u1 = (v0[1] * dx - v0[0] * dy) / den
        p = 0.5 * (p0 + v0 * u0 + p1 + v1 * u1)
    if u0 <= 0 and u1 >= 0:
        # Inner corner
        return [p]
    # Outer corner
    return [p0, p2, p1]

# This end cap function creates pointy caps.
def pointy(p0, v0, p1, v1):
    r = 0.5 * numpy.sqrt(numpy.sum((p0 - p1) ** 2))
    v0 /= numpy.sqrt(numpy.sum(v0 ** 2))
    v1 /= numpy.sqrt(numpy.sum(v1 ** 2))
    return [p0, 0.5 * (p0 + p1) + 0.5 * (v0 - v1) * r, p1]

# Paths with arbitrary offsets from the center and multiple layers.
sp3 = gdspy.FlexPath(
    [(0, 0), (0, 1)],
    [0.1, 0.3, 0.5],
    offset=[-0.2, 0, 0.4],
    layer=[0, 1, 2],
    corners=broken,
    ends=pointy,
)
sp3.segment((3, 3), offset=[-0.5, -0.1, 0.5])
sp3.segment((4, 1), width=[0.2, 0.2, 0.2], offset=[-0.2, 0, 0.2])
sp3.segment((0, -1), relative=True)

top_cell.add(sp3)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()