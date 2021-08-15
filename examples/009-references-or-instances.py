"""
Besides creating single references (also called instances) with gdspy.CellReference, 
it is possible to create full 2D arrays with a single entity using gdspy.CellArray.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

lib = gdspy.GdsLibrary()

# Layer/datatype definitions for each step in the fabrication
ld_fulletch = {"layer": 1, "datatype": 3}
ld_partetch = {"layer": 2, "datatype": 3}
ld_liftoff = {"layer": 0, "datatype": 7}

# Create polygons in different layers
p1 = gdspy.Rectangle((-3, -3), (3, 3), **ld_fulletch)
p2 = gdspy.Rectangle((-5, -3), (-3, 3), **ld_partetch)
p3 = gdspy.Rectangle((5, -3), (3, 3), **ld_partetch)
p4 = gdspy.Round((0, 0), 2.5, number_of_points=6, **ld_liftoff)

# Create a hole (or cutout)
cutout = gdspy.Polygon(
    [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0), (2, 2), (2, 3), (3, 3), (3, 2), (2, 2)])

# Create a cell with a component that is used repeatedly
contact = gdspy.Cell("CONTACT")
contact.add([p1, p2, p3, p4])

# Create a cell with the complete device
device = gdspy.Cell("DEVICE")

# Add the a hole reference (instance) in the device cell
device.add(cutout)

# Add 2 references to the component changing size and orientation
ref1 = gdspy.CellReference(contact, (3.5, 1), magnification=0.25)
ref2 = gdspy.CellReference(contact, (1, 3.5), magnification=0.25, rotation=90)
device.add([ref1, ref2])

# The final layout has several repetitions of the complete device
main = gdspy.Cell("MAIN")
main.add(gdspy.CellArray(device, 3, 2, (6, 7)))

# Display all cells using the internal viewer.
gdspy.LayoutViewer()