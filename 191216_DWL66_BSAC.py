import importlib
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
TriB = 200  # triangle base
TriH = 400  # triangle height
TriG = 300  # gap between triangles
# bscW = 30  # back side cross width
squareL = 30  # back side cross size
MarkN = 7  # number of Mark in one direction
pitchX = 10000  # pitch along X axis between Mark
pitchY = 10000  # pitch along Y axis between Mark
textS = 60  # text size
arrowS = 50  # arrow's size


# crosses
# --------------
# create top side cross cell
cell_Tri = gdspy.Cell('TSTri')
# layer1
TSTriLT = gdspy.Polygon([(-TriG/2-TriH, TriG/2+TriB/2),
                         (-TriG/2-TriH, TriG/2-TriB/2),
                         (-TriG/2, TriG/2)], layer=1)
TSTriRT = gdspy.Polygon([(TriG/2+TriH, TriG/2+TriB/2),
                         (TriG/2+TriH, TriG/2-TriB/2),
                         (TriG/2, TriG/2)], layer=1)
TSTriRB = gdspy.Polygon([(TriG/2+TriH, -TriG/2+TriB/2),
                         (TriG/2+TriH, -TriG/2-TriB/2),
                         (TriG/2, -TriG/2)], layer=1)
TSTriLB = gdspy.Polygon([(-TriG/2-TriH, -TriG/2+TriB/2),
                         (-TriG/2-TriH, -TriG/2-TriB/2),
                         (-TriG/2, -TriG/2)], layer=1)
cell_Tri.add(TSTriLT)
cell_Tri.add(TSTriRT)
cell_Tri.add(TSTriLB)
cell_Tri.add(TSTriRB)
# layer2
cell_BSTri = gdspy.Cell('BSTri')
BSTriLT = gdspy.Polygon([(-TriG/2-TriB/2, TriG/2+TriH),
                         (-TriG/2+TriB/2, TriG/2+TriH),
                         (-TriG/2, TriG/2)], layer=2)
BSTriRT = gdspy.Polygon([(+TriG/2-TriB/2, TriG/2+TriH),
                         (+TriG/2+TriB/2, TriG/2+TriH),
                         (+TriG/2, TriG/2)], layer=2)
BSTriRB = gdspy.Polygon([(+TriG/2-TriB/2, -TriG/2-TriH),
                         (+TriG/2+TriB/2, -TriG/2-TriH),
                         (+TriG/2, -TriG/2)], layer=2)
BSTriLB = gdspy.Polygon([(-TriG/2-TriB/2, -TriG/2-TriH),
                         (-TriG/2+TriB/2, -TriG/2-TriH),
                         (-TriG/2, -TriG/2)], layer=2)
cell_Tri.add(BSTriLT)
cell_Tri.add(BSTriRT)
cell_Tri.add(BSTriLB)
cell_Tri.add(BSTriRB)

# Arrow
# -----
# Arrows to show the position of the central mark
cell_Arrow = gdspy.Cell('Arrow')
L1_Arrow = gdspy.Polygon([(-arrowS/2, 0), (0, 2*arrowS), (arrowS/2, 0)],
                          layer = 1)
cell_Arrow.add(L1_Arrow)

# top
#----
cell_top = gdspy.Cell('top')
# add a circle representing a 4 inch wafer in the top cell in layer 0
wafer = gdspy.Round((0, 0), 50000, number_of_points=64, layer=0)
cell_top.add(wafer)
# add an array of Mark cell in the top cell
cell_top.add(gdspy.CellArray(cell_Tri, MarkN, MarkN,
                             (pitchX, pitchY),
                             (-pitchX*(MarkN-1)/2, -pitchY*(MarkN-1)/2)))
# add some arrows in the central part to show the position of the central mark
cell_top.add(gdspy.CellArray(cell_Arrow, 1, 15, (0, 300), (0, -4800)))
cell_top.add(gdspy.CellArray(cell_Arrow, 1, 15, (0, 300), (0, 4800),
                             rotation=180))

# write the coordinates of the alignment Mark in the top cell
for i in range(0, MarkN):
    for j in range(0, MarkN):
        # layer 1
        textPosition = (-pitchX*(MarkN-1)/2 -TriG/2-TriH + (i)*pitchX,
                        -pitchX*(MarkN-1)/2 + (j)*pitchY - textS/2)
        text = gdspy.Text((str(i)+','+str(j)), textS, textPosition, layer=1)
        cell_top.add(text)
        # layer 2
        textPosition = (-pitchX*(MarkN-1)/2 +TriG/2 -TriB/2  + (i)*pitchX,
                        -pitchX*(MarkN-1)/2 + (j)*pitchY - textS/2)
        text = gdspy.Text((str(i)+','+str(j)), textS, textPosition, layer=2)
        cell_top.add(text)

# Output
# ------
# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('191216_DWL66_BSAlignmentCalibration.gds', 
                unit=1.0e-6, precision=1.0e-9)

