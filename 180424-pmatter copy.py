import importlib
import numpy
import gdspy

# importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()

############################
# Define global parameters #
############################
c = 2300 # connector edge in um
r = ( (3 + numpy.sqrt(2)) / 2 ) * c # radius of the sphere in um
l1 = 0.278781*r
l2 = 0.355850*r
nL = 200 #notch length
nW = 50 #notch witdh / 2


# ------------------------------------------------------------------ #
#      POLYGONS
# ------------------------------------------------------------------ #

connector = gdspy.Rectangle((0,0), (c,c), 2)
notch1 = gdspy.Rectangle((0,0), (nL, nW), 1)
notch2 = gdspy.copy(notch1, c-nL, 0)
notch3 = gdspy.copy(notch1, c-nL, c-nW)
notch4 = gdspy.copy(notch1, 0, c-nW)
notch5 = gdspy.copy(notch1, nW, 0).rotate(numpy.pi/2, (nW, 0))
notch6 = gdspy.copy(notch1, c, 0).rotate(numpy.pi/2, (c, 0))
notch7 = gdspy.copy(notch1, c-nW, c).rotate(-numpy.pi/2, (c-nW, c))
notch8 = gdspy.copy(notch1, 0, c).rotate(-numpy.pi/2, (0, c))
connector_notches = [notch1, notch2, notch3, notch4, notch5, notch6, notch7, notch8]
connector_cell = lib.new_cell("connector")
connector_cell.add(gdspy.fast_boolean(connector, connector_notches, 'not', layer=1))
connector_6notches = [notch1, notch2, notch3, notch4, notch6, notch7]
connector_6notches_cell = lib.new_cell("connector_6notches")
connector_6notches_cell.add(gdspy.fast_boolean(connector, connector_6notches, 'not', layer=1))
connector_4notches = [notch1, notch2, notch5, notch6]
connector_4notches_cell = lib.new_cell("connector_4notches")
connector_4notches_cell.add(gdspy.fast_boolean(connector, connector_4notches, 'not', layer=1))

l1_rec = gdspy.Rectangle((0,0), (c,l1), 2)
l1_notch1 = notch1
l1_notch2 = gdspy.copy(notch1, c-nL, 0)
l1_notch3 = gdspy.copy(notch1, c-nL, l1-nW)
l1_notch4 = gdspy.copy(notch1, 0, l1-nW)
#l1_notch5 = gdspy.copy(notch1, nW, 0).rotate(numpy.pi/2, (nW, 0))
#l1_notch6 = gdspy.copy(notch1, c, 0).rotate(numpy.pi/2, (c, 0))
#l1_notch7 = gdspy.copy(notch1, c-nW, l1).rotate(-numpy.pi/2, (c-nW, l1))
#l1_notch8 = gdspy.copy(notch1, 0, l1).rotate(-numpy.pi/2, (0, l1))
l1_rec_4notches = [l1_notch1, l1_notch2, l1_notch3, l1_notch4]
l1_rec_cell = lib.new_cell("l1_rec")
l1_rec_cell.add(gdspy.fast_boolean(l1_rec, l1_rec_4notches, 'not', layer=1))
l1_rec_2notches = [l1_notch1, l1_notch2]
l1_rec_2notches_cell = lib.new_cell("l1_rec_2notches")
l1_rec_2notches_cell.add(gdspy.fast_boolean(l1_rec, l1_rec_2notches, 'not', layer=1))
l1_rec_60deg_cell = lib.new_cell("l1_rec_60deg")
#l1_rec_60deg_cell.add(gdspy.CellArray(l1_rec_2notches, 1, 1, (6, 7)))

main=lib.new_cell("main")
main.add(gdspy.CellArray(connector, 3, 2, (6, 7)))




# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('test.gds', unit=1.0e-6, precision=1.0e-9)
