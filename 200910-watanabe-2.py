import gdspy
import numpy

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

# constantes definitions
trenchW = 0.1 # trench width in um
trenchL = 1000 # trench length in um
nos = 20 # number of sections


# top cell creation
trenchesCell = lib.new_cell('trenches')
topCell = lib.new_cell('top')


# function to create a trench with n sections shifted by one trench width
def trench(trenchW, trenchL, nos):
  x = 0 # x position of a section's bottom left corner
  y = 0 # y position of a section's bottom left corner
  trenchCell = lib.new_cell("s"+str(int(trenchW*1000))+"nm") # creation of a trench cell
  for i in numpy.arange(nos):
    rect = gdspy.Rectangle((x, y), (x+trenchW, yY+l/sc), i)
    trenchCell.add(rect)
    x = x + trenchW
    y = y + trenchL/nos

# Save the library in a file called 'first.gds'.
lib.write_gds('201016-watanabe.gds')