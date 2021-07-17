import gdspy
import numpy

# constantes definitions
x = 0 # position to put the array
lineL = 1000 # line length
lineW = 1000
# pitch = 5*width
chipW = 10000
sections = 50
nlines = 5 # chipW*0.8/lineW # numbers of L/S for each parameters

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# top cell creation
trenchesCell = lib.new_cell('trenches')
topCell = lib.new_cell('top')

# function create a trench (the trench in line and trench)
def trench_creation(trenchW, l, sc):
  global x
  sectionX = 0
  sectionY = 0
  pitch = 5*trenchW
  nlines = chipW*0.8/pitch
  trenchCell = lib.new_cell("s"+str(int(trenchW*1000))+"nm")
  for i in numpy.arange(sc):
    rect = gdspy.Rectangle((sectionX, sectionY), (sectionX+trenchW, sectionY+l/sc), i)
    trenchCell.add(rect)
    sectionX = sectionX + trenchW
    sectionY = sectionY + l/sc
    # print(sectionX)
    # print(sectionY)
  trenchesCell.add(gdspy.CellArray(trenchCell, nlines, 1, (pitch, 0), (0, 0)))

for i in numpy.arange(0.1, 1.1, 0.1):
  trench_creation(i, lineL, sections)

topCell.add(gdspy.CellArray(trenchesCell, 9, 1, (chipW/10, 0), (chipW/10, 0)))

chipFrame = gdspy.Rectangle((0,0), (chipW, chipW), 0)
topCell.add(chipFrame)

# Save the library in a file
lib.write_gds('201016-watanabe.gds')