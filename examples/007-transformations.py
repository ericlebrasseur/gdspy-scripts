""" Create a rectangle and rotate it by pi/4
inspired from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy as np

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

poly = gdspy.Rectangle((-2, -2), (2, 2))
# create the same rectangle as poly and translate it by (0, 6)
poly2 = gdspy.Rectangle((-2, -2), (2, 2))
poly2.translate(0, 6)
# create the same rectangle as poly, translate by (0, 12)
# and rotate by pi/4 around it's center at (0, 12)
poly3 = gdspy.Rectangle((-2, -2), (2, 2))
poly3.translate(0, 12)
poly3.rotate(np.pi / 4, (0, 12))
# create the same rectangle as poly, translate by (0, 18),
# rotate by pi/4 around it's center and scale by (1, 0.5) around it's center
poly4 = gdspy.Rectangle((-2, -2), (2, 2))
poly4.translate(0, 18)
poly4.rotate(np.pi / 4, (0, 18))
poly4.scale(1, 0.5, (0, 18))
# create the same rectangle as poly, translate by (0, 24),
# rotate by pi/3 around it's center
poly5 = gdspy.Rectangle((-2, -2), (2, 2))
poly5.translate(0, 24)
poly5.rotate(np.pi / 3, (0, 24))
# same as poly5 + mirror about y-axis
poly6 = gdspy.Rectangle((-2, -2), (2, 2))
poly6.translate(0, 24)
poly6.rotate(np.pi / 3, (0, 24))
poly6.mirror((0,1), (0,0))

cell.add([poly, poly2, poly3, poly4, poly5, poly6])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()