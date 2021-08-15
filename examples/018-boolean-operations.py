"""
Boolean operations (gdspy.boolean()) can be performed on polygons, paths and whole cells.
from https://gdspy.readthedocs.io/en/stable/gettingstarted.html
"""

import gdspy
import numpy

lib = gdspy.GdsLibrary()

# Define layers
layer0 = {"layer": 0, "datatype": 0} # before boolean operation
layer1 = {"layer": 1, "datatype": 0} # after boolean operation
# click on the layer to display/hidden it

# Example of subtraction (not)

sub_cell = lib.new_cell('subtraction')

# Create some text
text = gdspy.Text("SUBTRACTION", 4, (0, 0), layer=0)
# Create a rectangle extending the text's bounding box by 1
bb = numpy.array(text.get_bounding_box())
rect = gdspy.Rectangle(bb[0] - 1, bb[1] + 1, layer=0)
# Subtract the text from the rectangle
sub = gdspy.boolean(rect, text, "not", layer=1)

sub_cell.add([text, rect, sub])


# Example of union (or)

union_cell = lib.new_cell('union')

# Create some text
text = gdspy.Text("UNION", 4, (0, 0), layer=0)
# Create a rectangle covering half the text
bb = numpy.array(text.get_bounding_box(),)
rect = gdspy.Rectangle(bb[0] - 1,
    [bb[1][0] + 1, bb[1][1] - (bb[1][1] - bb[0][1]) / 2],
    layer=0)

# Union of the text and the rectangle
uni = gdspy.boolean(rect, text, "or", layer=1)

union_cell.add([text, rect, uni])


# Example of intersection (and)

intersection_cell = lib.new_cell('intersection')

# Create some text
text = gdspy.Text("INTERSECTION", 4, (0, 0), layer=0)
# Create a rectangle covering half the text
bb = numpy.array(text.get_bounding_box())
rect = gdspy.Rectangle(bb[0] - 1,
    [bb[1][0] + 1, bb[1][1] - (bb[1][1] - bb[0][1]) / 2],
    layer=0)

# Union of the text and the rectangle
intersection = gdspy.boolean(rect, text, "and", layer=1)

intersection_cell.add([text, rect, intersection])


# Example of symmetric subtraction (xor)

sym_sub_cell = lib.new_cell('sym_subtraction')

# Create some text
text = gdspy.Text("SYM_SUB", 4, (0, 0), layer=0)
# Create a rectangle covering half the text
bb = numpy.array(text.get_bounding_box())
rect = gdspy.Rectangle(bb[0] - 1,
    [bb[1][0] + 1, bb[1][1] - (bb[1][1] - bb[0][1]) / 2],
    layer=0)

# Union of the text and the rectangle
sym_sub = gdspy.boolean(rect, text, "xor", layer=1)

sym_sub_cell.add([text, rect, sym_sub])


# Display all cells using the internal viewer.
gdspy.LayoutViewer(hidden_types=[(0, 0)])