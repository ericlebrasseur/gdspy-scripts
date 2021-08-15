"""
All shapes in the GDSII format are tagged with 2 properties: 
layer and datatype (or texttype in the case of gdspy.Label). 
They are always 0 by default, but can be any integer in the range from 0 to 255.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

lib = gdspy.GdsLibrary()
top_cell = lib.new_cell('top')

# Layer/datatype definitions for each step in the fabrication
ld_fulletch = {"layer": 1, "datatype": 3}
ld_partetch = {"layer": 2, "datatype": 3}
ld_liftoff = {"layer": 0, "datatype": 7}

# Create polygons in different layers
p1 = gdspy.Rectangle((-3, -3), (3, 3), **ld_fulletch)
p2 = gdspy.Rectangle((-5, -3), (-3, 3), **ld_partetch)
p3 = gdspy.Rectangle((5, -3), (3, 3), **ld_partetch)
p4 = gdspy.Round((0, 0), 2.5, number_of_points=6, **ld_liftoff)

top_cell.add([p1, p2, p3, p4])

# Display all cells using the internal viewer.
gdspy.LayoutViewer()