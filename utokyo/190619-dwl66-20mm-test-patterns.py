import importlib
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
lineL_L1 = 2500  # line length in um for layer 1
lineL_L2 = 200  # line length in um for layer 2
lineN = 5  # number of lines in an group of line of same widths
lineWList = [1.0, 2.0, 3.0, 4.0, 5.0]  # list of line widths
lineP = 15  # pitch between lines in a same group
layerG = 2  # The gap between layer 1 and layer 2 lines
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
    line_L1 = gdspy.Rectangle((0, lineL_L2 + layerG),
                              (lineW, lineL_L2 + layerG + lineL_L1), layer=1)
    # Create a line in layer 2 positionned bellow the line in layer 1
    # The gap between layer 1 and layer 2 lines is layerG
    # The bottom left is at the origin
    line_L2 = gdspy.Rectangle((0, 0), (lineW, lineL_L2), layer=2)
    cell_line = gdspy.Cell(cellname)  # Create a line cell
    cell_line.add(line_L1)  # Put layer 1 line into the line cell
    cell_line.add(line_L2)  # put layer 2 line into the line cell
    cell_lineArray.append(cell_line)  # Put the line cell into
    # the python line array

# Create a python array of spaces. One space for each line width in lineWList.
# Space widths are the same as line widths
cell_spaceArray = []  # Create an empty array of space cells
for lineW in lineWList:  # Fill the empty array of spaces
    cellname = 'space' + str(lineW) + 'um'
    # Create a space in layer 1:
    space_L1 = gdspy.Rectangle((lineW, lineL_L2 + layerG),
                               (lineP, lineL_L2 + layerG + lineL_L1), layer=1)
    # Create a space in layer 2 positionned bellow the space in layer 1
    # The gap between layer 1 and layer 2 space is layerG
    # The space bottom left is at the origin
    space_L2 = gdspy.Rectangle((lineW, 0), (lineP, lineL_L2), layer=2)
    cell_space = gdspy.Cell(cellname)  # Create a space cell
    cell_space.add(space_L1)  # Put layer 1 space into the space cell
    cell_space.add(space_L2)  # put layer 2 space into the space cell
    cell_spaceArray.append(cell_space)  # Put the space cell into
    # the python space array


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
    originX = originX + lineP*(lineN+1)
    origin = (originX, textS + textG)  # Position of the first line.
    # Add a row of lineN cell_line instances in the top cell:
    # class gdspy.CellArray(ref_cell, columns, rows, spacing, origin,
    # rotation, magnification, x_reflection, ignore_missing)
    cell_top1.add(gdspy.CellArray(cell_line, lineN, 1, pitch, origin))
    # Write the line width above and bellow the lines:
    textPosition = (originX, lineL_L1 + lineL_L2 + textS + 2*textG)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (originX, 0)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)

# Create a group of lineN lines
# for each value of line width in lineWList.
# The pitch between lines is lineP.
for cell_line in cell_lineArray:
    i = cell_lineArray.index(cell_line)
    pitch = (lineP, 0)
    originX = originX + lineP*(lineN+1)
    origin = (originX, textS + textG)
    # Add a row of lineN cell_line instances in the top cell:
    # class gdspy.CellArray(ref_cell, columns, rows, spacing, origin,
    # rotation, magnification, x_reflection, ignore_missing)
    cell_top1.add(gdspy.CellArray(cell_line, lineN, 1, pitch, origin))
    # Write the line width above and bellow the lines:
    textPosition = (originX, lineL_L1 + lineL_L2 + textS + 2*textG)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (originX, 0)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)

# Create a group of lineN spaces
# for each value of line width in lineWList.
# The pitch between spaces is lineP.
for cell_space in cell_spaceArray:
    i = cell_spaceArray.index(cell_space)
    pitch = (lineP, 0)
    originX = originX + lineP*(lineN+1)
    origin = (originX, textS + textG)
    # Add a row of lineN cell_line instances in the top cell:
    # class gdspy.CellArray(ref_cell, columns, rows, spacing, origin,
    # rotation, magnification, x_reflection, ignore_missing)
    cell_top1.add(gdspy.CellArray(cell_space, lineN, 1, pitch, origin))
    # Write the line width above and bellow the lines:
    textPosition = (originX, lineL_L1 + lineL_L2 + textS + 2*textG)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (originX, 0)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)

# add a large surface that can be use to measure the thickness with dektak
originX = originX + lineP*(lineN+1)
topCellH = cell_top1.get_bounding_box()[1][1]  # top1 cell height
largeSurf_L1 = gdspy.Rectangle((originX, 2*topCellH/3),
                               (originX + largeSurfL, 2*topCellH/3 +
                                largeSurfW), layer=1)
largeSurf2_L1 = gdspy.Rectangle((originX + largeSurfL/2 - largeSurfW/2,
                                 2*topCellH/3 - largeSurfL/2 + largeSurfW/2),
                                (originX + largeSurfL/2 + largeSurfW/2,
                                2*topCellH/3 + largeSurfL/2 + largeSurfW/2),
                                layer=1)
largeSurf_L2 = gdspy.Rectangle((originX, topCellH/3),
                               (originX + largeSurfL, topCellH/3 +
                                largeSurfW), layer=2)
largeSurf2_L2 = gdspy.Rectangle((originX + largeSurfL/2 - largeSurfW/2,
                                 topCellH/3 - largeSurfL/2 + largeSurfW/2),
                                (originX + largeSurfL/2 + largeSurfW/2,
                                topCellH/3 + largeSurfL/2 + largeSurfW/2),
                                layer=2)
cell_top1.add(largeSurf_L1)
cell_top1.add(largeSurf2_L1)
cell_top1.add(largeSurf_L2)
cell_top1.add(largeSurf2_L2)

topCellW = cell_top1.get_bounding_box()[1][0]  # top1 cell width

# copy the top1 cell into top cell and center it on the origin or coordinates:
cell_top = gdspy.Cell('top')
origin = (- topCellW/2, - topCellH/2)
cell_top.add(gdspy.CellArray(cell_top1, 1, 1, (0, 0), origin))




# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('190619-dwl66-20mm-test-patterns.gds', unit=1.0e-6, precision=1.0e-9)
