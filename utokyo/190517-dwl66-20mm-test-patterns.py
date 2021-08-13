import importlib
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
lineL = 100  # line length in um
lineN = 5  # number of lines in an array
lineWList = [1.6, 2.0, 2.4, 2.8, 3.0, 3.2, 3.6, 4.0, 5.0]  # list of line widths
lineP = 15  # pitch between lines in a same array
arrayP = 100  # pitch between arrays of lines
yP = 2*lineL + 100   # pitch between lines of arrays of lines
textS = 15  # text size in um
cellW = arrayP*(len(lineWList)-1) + lineP*lineN  # cell width
cellL = 2*(yP + lineL + 10 + textS)
cellG = 50  # gap between cells

# ------------------------------------------------------------------ #
#      basic lines
# ------------------------------------------------------------------ #

cell_lineArray = []
for lineW in lineWList:
    cellname = 'line' + str(lineW) + 'um'
    lineL1 = gdspy.Rectangle((0, 1), (lineW, lineL), layer=1)
    lineL2 = gdspy.Rectangle((0, -1-lineL), (lineW, -1), layer=2)
    cell_line = gdspy.Cell(cellname)
    cell_line.add(lineL1)
    cell_line.add(lineL2)
    cell_lineArray.append(cell_line)
cell_spaceArray = []
for lineW in lineWList:
    cellname = 'space' + str(lineW) + 'um'
    spaceL1 = gdspy.Rectangle((lineW, 1), (lineP, lineL), layer=1)
    spaceL2 = gdspy.Rectangle((lineW, -1-lineL), (lineP, -1), layer=2)
    cell_space = gdspy.Cell(cellname)
    cell_space.add(spaceL1)
    cell_space.add(spaceL2)
    cell_spaceArray.append(cell_space)


# ------------------------------------------------------------------ #
#      top cell
# ------------------------------------------------------------------ #

cell_top1 = gdspy.Cell('top1')
for cell_line in cell_lineArray:
    i = cell_lineArray.index(cell_line)
    spacing = (lineWList[i]*2, 0)
    origin = (i*arrayP - cellW/2, yP)
    cell_top1.add(gdspy.CellArray(cell_line, 5, 1, spacing, origin))
    textPosition = (i*arrayP - cellW/2, yP + lineL + 10)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (i*arrayP - cellW/2, yP - lineL - 10 - textS)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)
for cell_line in cell_lineArray:
    i = cell_lineArray.index(cell_line)
    spacing = (lineP, 0)
    origin = (i*arrayP - cellW/2, 0)
    cell_top1.add(gdspy.CellArray(cell_line, 5, 1, spacing, origin))
    textPosition = (i*arrayP - cellW/2, lineL + 10)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (i*arrayP - cellW/2, -lineL - 10 - textS)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)
for cell_space in cell_spaceArray:
    i = cell_spaceArray.index(cell_space)
    spacing = (lineP, 0)
    origin = (i*arrayP - cellW/2, -yP)
    cell_top1.add(gdspy.CellArray(cell_space, 5, 1, spacing, origin))
    textPosition = (i*arrayP - cellW/2, -yP + lineL + 10)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=1)
    cell_top1.add(text)
    textPosition = (i*arrayP - cellW/2, -yP - lineL - 10 - textS)
    text = gdspy.Text(str(lineWList[i]), textS, textPosition, layer=2)
    cell_top1.add(text)

cell_top = gdspy.Cell('top')
totalW = cellW + cellL + cellG
pos1 = (-totalW/2 + cellW/2, 0)
pos2 = (cellW/2 + yP + lineL + textS + 10 + cellG - totalW/2 + cellW/2, 0)
cell_top.add(gdspy.CellReference(cell_top1, pos1))
cell_top.add(gdspy.CellReference(cell_top1, pos2, rotation=90))


# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('190517-dwl66-20mm-test-patterns.gds', unit=1.0e-6, precision=1.0e-9)
