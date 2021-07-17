import importlib
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
tscW = 1  # top side cross with
tscL = 2.5  # top side cross length layer1
bscW = 30  # back side cross width
bscL = 30  # back side cross length
marksN = 7  # number of marks in one direction
pitchX = 10000  # pitch along X axis between marks
pitchY = 10000  # pitch along Y axis between marks
textS = 30  # text size


# top side cross
# --------------
# create top side cross cell
cell_topSideCross = gdspy.Cell('topSideCross')
# layer1
L1_Rect1 = gdspy.Rectangle((-2*tscL, -tscW/2), (-tscL, tscW/2), layer=1)
L1_Rect2 = gdspy.Rectangle((-tscW/2, tscL), (tscW/2, 2*tscL), layer=1)
L1_Rect3 = gdspy.Rectangle((tscL, -tscW/2), (2*tscL, tscW/2), layer=1)
L1_Rect4 = gdspy.Rectangle((-tscW/2, -2*tscL), (tscW/2, -tscL), layer=1)
L1_Poly1 = gdspy.Polygon([(-tscW/2, 2*tscL),
                       (0, 2*tscL+tscW),
                       (tscW/2, 2*tscL)], layer=1)
# add polygons into the top side cross cell
cell_topSideCross.add(L1_Rect1)
cell_topSideCross.add(L1_Rect2)
cell_topSideCross.add(L1_Rect3)
cell_topSideCross.add(L1_Rect4)
cell_topSideCross.add(L1_Poly1)
# layer2
L2_Poly1 = gdspy.Polygon([(-tscL, -tscW/2),
                         (-tscL, tscW/2),
                         (-tscW/2, tscW/2),
                         (-tscW/2, tscL),
                         (tscW/2, tscL),
                         (tscW/2, tscW/2),
                         (tscL, tscW/2),
                         (tscL, -tscW/2),
                         (tscW/2, -tscW/2),
                         (tscW/2, -tscL),
                         (-tscW/2, -tscL),
                         (-tscW/2, -tscW/2)], layer=2)
# add polygons into the top side cross cell
cell_topSideCross.add(L2_Poly1)

# back side cross
#----------------
# create back side cross cell
cell_backSideCross = gdspy.Cell('backSideCross')
# layer1
L1_Rect1 = gdspy.Rectangle((-3*bscL/2, -bscL/2), (-bscL/2, bscL/2), layer=1)
L1_Rect2 = gdspy.Rectangle((-bscL/2, bscL/2), (bscL/2, 3*bscL/2), layer=1)
L1_Rect3 = gdspy.Rectangle((bscL/2, -bscL/2), (3*bscL/2, bscL/2), layer=1)
L1_Rect4 = gdspy.Rectangle((-bscL/2, -3*bscL/2), (bscL/2, -bscL/2), layer=1)
L1_Poly1 = gdspy.Polygon([(-bscL/2, 3*bscL/2),
                          (0, 2*bscL),
                          (bscL/2, 3*bscL/2)], layer=1)
# add polygons into the back side cross cell
cell_backSideCross.add(L1_Rect1)
cell_backSideCross.add(L1_Rect2)
cell_backSideCross.add(L1_Rect3)
cell_backSideCross.add(L1_Rect4)
cell_backSideCross.add(L1_Poly1)
# layer2
L2_Rect1 = gdspy.Rectangle((-bscL/2, -bscL/2), (bscL/2, bscL/2), layer=2)
# add polygons into the back side cross cell
cell_backSideCross.add(L2_Rect1)


# marks
# -----
# create marks cell
cell_marks = gdspy.Cell('marks')
# add top side cross cell into marks cell
cell_marks.add(gdspy.CellArray(cell_topSideCross, 1, 1, (0, 0), (0, 0), 0, 10))
cell_marks.add(gdspy.CellArray(cell_topSideCross, 1, 1, (0, 0), (200, 0), 0, 1))
cell_marks.add(gdspy.CellArray(cell_topSideCross, 1, 1, (0, 0), (100, 0), 0, 5))
# add back side cross cell into marks cell
cell_marks.add(gdspy.CellArray(cell_backSideCross, 1, 1, (0, 0), (200, 100), 0, 1))

# top
#----
cell_top = gdspy.Cell('top')
# add a circle representing a 4 inch wafer in the top cell in layer 0
wafer = gdspy.Round((0, 0), 50000, number_of_points=64, layer=0)
cell_top.add(wafer)
# add an array of marks cell in the top cell
cell_top.add(gdspy.CellArray(cell_marks, marksN, marksN,
                             (pitchX, pitchY),
                             (-pitchX*(marksN-1)/2, -pitchY*(marksN-1)/2)))

# write the coordinates of the alignment marks in the top cell
for i in range(0, marksN):
    for j in range(0, marksN):
        # layer 1
        textPosition = (-pitchX*(marksN-1)/2 + (i)*pitchX,
                        -pitchX*(marksN-1)/2 + (j)*pitchY + 120)
        text = gdspy.Text((str(i)+','+str(j)), textS, textPosition, layer=1)
        cell_top.add(text)
        # layer 2
        textPosition = (-pitchX*(marksN-1)/2 + (i)*pitchX,
                        -pitchX*(marksN-1)/2 + (j)*pitchY + 70)
        text = gdspy.Text((str(i)+','+str(j)), textS, textPosition, layer=2)
        cell_top.add(text)

# Output
# ------
# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('190702_dwl66_AlignmentMarks.gds', 
                unit=1.0e-6, precision=1.0e-9)
