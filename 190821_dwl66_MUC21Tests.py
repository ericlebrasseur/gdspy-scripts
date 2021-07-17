import importlib
import gdspy
import math

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
lineL_L1 = 2500  # line length in um for layer 1
lineN = 5  # number of lines in an group of line of same widths
lineWList = [5, 10, 15, 20, 30, 50]  # list of line widths
lineG = 50  # gap between groups of line
textS = 30  # text size in um
textG = 10  # gap between text and lines
largeSurfL = 500  # large surface length
largeSurfW = 100  # large surface width

# ------------------------------------------------------------------ #
#      basic lines
# ------------------------------------------------------------------ #

# Create a python array of lines. One line for each line width in lineWList.
cell_lineArray = []  # Create an empty array of line cells
for lineW in lineWList:  # Fill the empty array of lines
    cellname = 'line' + str(lineW) + 'um'
    # Create a line in layer 1:
    line_L1 = gdspy.Rectangle((0, 0), (lineW, lineL_L1), layer=1)
    cell_line = gdspy.Cell(cellname)  # Create a line cell
    cell_line.add(line_L1)  # Put layer 1 line into the line cell
    cell_lineArray.append(cell_line)  # Put the line cell into
    # the python line array

# ------------------------------------------------------------------ #
#      top cell
# ------------------------------------------------------------------ #

cell_top1 = gdspy.Cell('top1')  # Top cell before translation
# Create a group of lineN lines and spaces
# for each value of line width in lineWList.
# The gap between lines is the same as the line width.
originX = 0  # Abcisse of the first line in a group of lineN lines
for cell_line in cell_lineArray:
    i = cell_lineArray.index(cell_line)
    pitch = (lineWList[i]*2, 0)  # Pitch between 2 lines in a group.
    origin = (originX, textG)  # Position of the first line.
    # Add a row of lineN cell_line instances in the top cell:
    # class gdspy.CellArray(ref_cell, columns, rows, spacing, origin,
    # rotation, magnification, x_reflection, ignore_missing)
    cell_top1.add(gdspy.CellArray(cell_line, lineN, 1, pitch, origin))
    # Write the line width above and bellow the lines:
    textPosition = (originX + textS, lineL_L1 + 2*textG)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition,
                      angle=math.pi/2, layer=1)
    cell_top1.add(text)
    textPosition = (originX, 0)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition,
                      angle=-math.pi/2, layer=1)
    cell_top1.add(text)
    originX = originX + lineWList[i]*2*(lineN+1) + lineG


# add a large surface that can be use to measure the thickness with dektak
topCellW = cell_top1.get_bounding_box()[1][0]  # top1 cell width
topCellH = cell_top1.get_bounding_box()[1][1]  # top1 cell height
originX = topCellW + lineG
largeSurf_L1 = gdspy.Rectangle((originX, largeSurfL/2),
                               (originX + largeSurfL, largeSurfL/2 +
                                largeSurfW), layer=1)
largeSurf2_L1 = gdspy.Rectangle((originX + largeSurfL/2 - largeSurfW/2,
                                 largeSurfL/2 - largeSurfL/2 + largeSurfW/2),
                                (originX + largeSurfL/2 + largeSurfW/2,
                                largeSurfL/2 + largeSurfL/2 + largeSurfW/2),
                                layer=1)
largeSurf3_L1 = gdspy.Rectangle((originX, 2*largeSurfL),
                               (originX + largeSurfL, 4*largeSurfL), layer=1)

cell_top1.add(largeSurf_L1)
cell_top1.add(largeSurf2_L1)

topCellW = cell_top1.get_bounding_box()[1][0]  # top1 cell width
topCellH = cell_top1.get_bounding_box()[1][1]  # top1 cell height

# copy the top1 cell into top cell and center it on the origin or coordinates:
cell_top = gdspy.Cell('top')
origin = (- topCellW/2, - topCellH/2)
cell_top.add(gdspy.CellArray(cell_top1, 1, 1, (0, 0), origin))




# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('test.gds', unit=1.0e-6, precision=1.0e-9)
