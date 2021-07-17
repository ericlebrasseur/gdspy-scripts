import importlib
import numpy
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

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
connector_cell = gdspy.Cell('connector')
connector_cell.add(gdspy.fast_boolean(connector, connector_notches, 'not', layer=1))
connector_6notches = [notch1, notch2, notch3, notch4, notch6, notch7]
connector_6notches_cell = gdspy.Cell('connector_6notches')
connector_6notches_cell.add(gdspy.fast_boolean(connector, connector_6notches, 'not', layer=1))
connector_4notches = [notch1, notch2, notch5, notch6]
connector_4notches_cell = gdspy.Cell('connector_4notches')
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
l1_rec_cell = gdspy.Cell('l1_rec')
l1_rec_cell.add(gdspy.fast_boolean(l1_rec, l1_rec_4notches, 'not', layer=1))
l1_rec_2notches = [l1_notch1, l1_notch2]
l1_rec_2notches_cell = gdspy.Cell('l1_rec_2notches')
l1_rec_2notches_cell.add(gdspy.fast_boolean(l1_rec, l1_rec_2notches, 'not', layer=1))
l1_rec_60deg_cell = gdspy.Cell('l1_rec_60deg')
l1_rec_60deg_cell.add(gdspy.CellArray('l1_rec_2notches', 1, 1, (0, 0), rotation=60))
l1_rec_120deg_xref_cell = gdspy.Cell('l1_rec_120deg_xref')
l1_rec_120deg_xref_cell.add(gdspy.CellArray('l1_rec_2notches', 1, 1, (0, 0), rotation=120.001, x_reflection=True))
l1_rec_m60deg_xref_cell = gdspy.Cell('l1_rec_m60deg_xref')
l1_rec_m60deg_xref_cell.add(gdspy.CellArray('l1_rec_2notches', 1, 1, (0, 0), rotation=-59.999, x_reflection=True))
l1_rec_60deg_xref_cell = gdspy.Cell('l1_rec_60deg_xref')
l1_rec_60deg_xref_cell.add(gdspy.CellArray('l1_rec_2notches', 1, 1, (0, 0), rotation=-120.001))

l2_rec = gdspy.Rectangle((0,0), (c,l2), 2)
l2_notch1 = notch1
l2_notch2 = gdspy.copy(notch1, c-nL, 0)
l2_notch3 = gdspy.copy(notch1, c-nL, l2-nW)
l2_notch4 = gdspy.copy(notch1, 0, l2-nW)
l2_rec_4notches = [l2_notch1, l2_notch2, l2_notch3, l2_notch4]
l2_rec_cell = gdspy.Cell('l2_rec')
l2_rec_cell.add(gdspy.fast_boolean(l2_rec, l2_rec_4notches, 'not', layer=1))
l2_rec_90deg_cell = gdspy.Cell('l2_rec_90deg')
l2_rec_90deg_cell.add(gdspy.CellArray('l2_rec', 1, 1, (0, 0), rotation=90))
l2_rec_2notches = [l2_notch1, l2_notch2]
l2_rec_2notches_cell = gdspy.Cell('l2_rec_2notches')
l2_rec_2notches_cell.add(gdspy.fast_boolean(l2_rec, l2_rec_2notches, 'not', layer=1))


points = [(0, 0), (c, 0), (c/2, c*numpy.sin(60*numpy.pi/180))]
triangle = gdspy.Polygon(points, 2)
tri_notch1 = notch1
tri_notch2 = gdspy.copy(notch1, 0, -nW).rotate(numpy.pi/3, (0, 0))
tri_notch3 = gdspy.copy(notch1, c, nW).rotate(numpy.pi, (c, nW))
tri_notch4 = gdspy.copy(notch1, c, 0).rotate(2*numpy.pi/3, (c, 0))
tri_notch5 = gdspy.copy(notch1, c/2, c*numpy.sin(numpy.pi/3) - nW).rotate(-numpy.pi/3, (c/2, c*numpy.sin(numpy.pi/3)))
tri_notch6 = gdspy.copy(notch1, c/2, c*numpy.sin(numpy.pi/3)).rotate(3.999*numpy.pi/3, (c/2, c*numpy.sin(numpy.pi/3)))
triangle_notches = [tri_notch1, tri_notch2, tri_notch3, tri_notch4, tri_notch5, tri_notch6]
triangle_cell = gdspy.Cell('triangle')
#triangle_cell.add(triangle_notches)
#triangle_cell.add(triangle)
triangle_cell.add(gdspy.fast_boolean(triangle, triangle_notches, 'not', layer=1))


# ------------------------------------------------------------------ #
#      TOP CELL
# ------------------------------------------------------------------ #

top_cell = gdspy.Cell('top')

# Here we subtract the previously created spiral from a rectangle with
# the 'not' operation.
top_cell.add(gdspy.CellArray('connector_6notches', 1, 1, (0, 0), (0, 0)))
top_cell.add(gdspy.CellArray('connector_6notches', 1, 1, (0, 0), (8*c+7*l2, 0), rotation=180, x_reflection=True))
top_cell.add(gdspy.CellArray('connector', 6, 1, (c+l2, 0), (c+l2, 0)))
top_cell.add(gdspy.CellArray('connector', 4, 2, (2*(c+l2), 2*(c+l2)), (c+l2, -(c+l2))))
top_cell.add(gdspy.CellArray('connector', 1, 1, (0, 0), (c+l2, -2*(c+l2))))
top_cell.add(gdspy.CellArray('connector', 1, 1, (0, 0), (5*(c+l2), 2*(c+l2))))

top_cell.add(gdspy.CellArray('l1_rec', 4, 2, (2*(c+l2), c+l1), (0, -l1)))
top_cell.add(gdspy.CellArray('l1_rec_60deg', 4, 1, (2*(c+l2), 0), (0, c+l1)))
top_cell.add(gdspy.CellArray('l1_rec_120deg_xref', 4, 1, (2*(c+l2), 0), (c, c+l1)))
top_cell.add(gdspy.CellArray('l1_rec_m60deg_xref', 4, 1, (2*(c+l2), 0), (0, -l1)))
top_cell.add(gdspy.CellArray('l1_rec_60deg_xref', 4, 1, (2*(c+l2), 0), (c, -l1)))

top_cell.add(gdspy.CellArray('l2_rec', 4, 4, (2*(c+l2), c+l2), (c+l2, -(c+2*l2))))
top_cell.add(gdspy.CellArray('l2_rec_90deg', 8, 1, (c+l2, 0), (c+l2, 0)))

top_cell.add(gdspy.CellArray('triangle', 4, 1, (2*(c+l2), 0), (0, c+l1)))
top_cell.add(gdspy.CellArray('triangle', 4, 1, (2*(c+l2), 0), (0, -l1), x_reflection=True))



# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('gdspy_test180605.gds', unit=1.0e-6, precision=1.0e-9)
