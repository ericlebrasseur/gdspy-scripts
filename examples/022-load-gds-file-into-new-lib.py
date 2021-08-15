"""
load a GDSII file into a new library
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy

# Load a GDSII file into a new library
gdsii = gdspy.GdsLibrary(infile='examples/001-create-rect-cell-and-save-in-file.gds')
top_cell = gdsii.top_level()[0]
text = gdspy.Text("Load a GDSII file into a new library", 2, (0, 2))
top_cell.add(text)

# Display all cells using the internal viewer.
gdspy.LayoutViewer()