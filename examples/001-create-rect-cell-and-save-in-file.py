""" Create a library (= a gds file), a new cell,
a rectangle, put the rectangle in the cell,
save to gds file, svg file and display in internal viewer
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
cell = lib.new_cell('top')

# Create the geometry (a single rectangle) and add it to the cell.
rect = gdspy.Rectangle((0, 0), (2, 1))
cell.add(rect)

# Save the library in a file called 'first.gds'.
lib.write_gds('001-create-rect-cell-and-save-in-file.gds')

# Optionally, save an image of the cell as SVG.
cell.write_svg('001-create-rect-cell-and-save-in-file.svg')

# Display all cells using the internal viewer.
gdspy.LayoutViewer()
