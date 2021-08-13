import gdspy
import numpy

# constantes definitions
nlines = 5 # numbers of L/S for each parameters
x = 0 # position to put the array
l = 10000 # line length
pitch = 3
chipW = 10000

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# top cell creation
trenchesCell = lib.new_cell('trenches')
topCell = lib.new_cell('top')

# function create a trench (the trench in line and trench)
def trench_creation(trenchW):
  global x
  trenchCell = lib.new_cell("s"+str(int(trenchW*1000))+"nm")
  rect = gdspy.Rectangle((0,0), (trenchW, l), 1)
  trenchCell.add(rect)
  trenchesCell.add(gdspy.CellArray(trenchCell, nlines, 1, (pitch, 0), (x, 0)))
  x = x + nlines*(pitch+trenchW) + pitch

for i in numpy.arange(0.1, 1.1, 0.1):
  trench_creation(i)

topCell.add(gdspy.CellArray(trenchesCell, 9, 1, (chipW/10, 0), (chipW/10, 0)))

chipFrame = gdspy.Rectangle((0,0), (chipW, chipW), 0)
topCell.add(chipFrame)

# Save the library in a file called 'first.gds'.
lib.write_gds('200820-watanabe.gds')