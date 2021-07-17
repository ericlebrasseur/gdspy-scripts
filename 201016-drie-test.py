import gdspy
import numpy

# constantes definitions
trenchL = 8000 # trench length
chipS = 8000 # size of a square chip
arrayX = 0 # X coordinate of an array of trenches

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# top cell creation
trenchCellA = lib.new_cell('trenches') # array of trenches cells
topCell = lib.new_cell('top')

trenchCells = {} # dictionary or trench cells

# function to create a trench cell
def trench_creation(trenchW, trenchL):
  cellName = "s"+str(int(trenchW*1000))+"nm"
  trenchCells[str(trenchW)] = lib.new_cell(cellName)
  rect = gdspy.Rectangle((0,0), (trenchW, trenchL), 1)
  trenchCells[str(trenchW)].add(rect)

# creation of trench cells
for trenchW in [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]: 
  trench_creation(trenchW, trenchL)

# adding arrays of trench cells in the trenchCellA cell

#L/S = 1/1
trenchN = 5 # numbers of trenches (in an array of trenches) for each parameters
trenchAG = 20 # gap between arrays of trenches

# adding arrays of trench cells in the trenchCellA cell
for trenchW in [0.1, 0.2, 0.5, 1, 2, 5]:
  trenchP = 2*trenchW
  trenchCellA.add(gdspy.CellArray(trenchCells[str(trenchW)], trenchN, 1, (trenchP, 0), (arrayX, 0)))
  arrayX = arrayX + trenchN*trenchP + trenchAG

# trenches are well separated to avoid collapse of mesas
trenchP = 10 # pitch between trenches

for trenchW in [0.1, 0.2, 0.5, 1, 2, 5]:
  trenchCellA.add(gdspy.CellArray(trenchCells[str(trenchW)], trenchN, 1, (trenchP, 0), (arrayX, 0)))
  arrayX = arrayX + trenchN*trenchP + trenchAG

trenchN = 3

for trenchW in [10, 20, 50, 100]:
  trenchP = 2*trenchW
  trenchAG = trenchW
  trenchCellA.add(gdspy.CellArray(trenchCells[str(trenchW)], trenchN, 1, (trenchP, 0), (arrayX, 0)))
  arrayX = arrayX + trenchN*trenchP + trenchAG

trenchN = 1
trenchAG = 0

for trenchW in [200]:
  trenchP = 2*trenchW
  trenchCellA.add(gdspy.CellArray(trenchCells[str(trenchW)], trenchN, 1, (trenchP, 0), (arrayX-trenchW/2, 0)))
  arrayX = arrayX + (trenchN-1)*trenchP + trenchN*trenchW + trenchAG

topCell.add(gdspy.CellArray(trenchCellA, 4, 1, (arrayX, 0), (0, 0)))

chipFrame = gdspy.Rectangle((0,0), (chipS, chipS), 0)
topCell.add(chipFrame)

# Save the library in a file called 'first.gds'.
lib.write_gds('201019-drie-test.gds')