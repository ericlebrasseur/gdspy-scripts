import gdspy
import numpy

# constantes definitions
trenchN = 5 # numbers of trenches (in an array of trenches) for each parameters
trenchL = 8000 # line length
trenchP = 10 # pitch between trenches
trenchAP = 10 # pitch between arrays of trenches
chipS = 8000 # size of a square chip
arrayX = 0 # X coordinate of an array of trenches

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# top cell creation
trenchesCell = lib.new_cell('trenches')
topCell = lib.new_cell('top')

# function create a trench (the trench in line and trench)
def trench_creation(trenchW, trenchN, trenchP, trenchAP):
  global arrayX
  cellName = "s"+str(int(trenchW*1000))+"nm"
  trenchCell = lib.new_cell(cellName)
  rect = gdspy.Rectangle((0,0), (trenchW, trenchL), 1)
  trenchCell.add(rect)
  trenchesCell.add(gdspy.CellArray(trenchCell, trenchN, 1, (trenchP, 0), (arrayX, 0)))
  arrayX = arrayX + (trenchN-1)*trenchP+trenchN*trenchW + trenchAP

for trenchW in [0.1, 0.2, 0.5, 1, 2, 5, 10, 20]:
  trench_creation(trenchW, trenchN, trenchW*3, trenchAP)

trenchN = 1
trenchP = 0
trenchAP = 100

for trenchW in [50, 100, 200]:
  trench_creation(trenchW, trenchN, trenchP, trenchAP)

trenchN = 5
trenchAP = 10


topCell.add(gdspy.CellArray(trenchesCell, 2, 1, (0, 0), (chipS/10, 0)))

chipFrame = gdspy.Rectangle((0,0), (chipS, chipS), 0)
topCell.add(chipFrame)

# Save the library in a file called 'first.gds'.
lib.write_gds('201016-drie-test.gds')