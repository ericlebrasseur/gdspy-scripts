import importlib
import gdspy

importlib.reload(gdspy)

print('Using gdspy module version ' + gdspy.__version__)

############################
# Define global parameters #
############################
MarkW = 10 # Top side Mark with
MarkL = 100  # Top side Mark length layer1
Shift = 0.5 # Shift of the Mark from the origin to take into account the 
            # width widening after development
Shift2 = 50 # Shift of the 4 marks from the origin
#bscW = 30  # back side Mark width
# squareL = 30  # back side Mark size
MarkN = 7  # number of Mark in one direction
pitchX = 10000  # pitch along X axis between Mark
pitchY = 10000  # pitch along Y axis between Mark
textS = 100  # text size
arrowS= 50  # arrow's size


# Marks
# --------------
# create Top side Marks cell (without triangle)
cell_Mark1 = gdspy.Cell('Mark1')
# layer1
L1_Rect1 = gdspy.Rectangle((-MarkL-Shift, -MarkW-Shift),
                           (-Shift, -Shift), layer=1)
L1_Rect2 = gdspy.Rectangle((Shift, Shift), (MarkW+Shift, MarkL+Shift), layer=1)

# add polygons into the Mark cell
cell_Mark1.add(L1_Rect1)
cell_Mark1.add(L1_Rect2)

# create Top side Mark2 cell (with triangle)
cell_Mark2 = gdspy.Cell('Mark2')
# layer1
L1_Tri1 = gdspy.Polygon([(Shift, Shift+MarkL),
                       (Shift+MarkW/2, Shift+MarkL+MarkW),
                       (Shift+MarkW, Shift+MarkL)], layer=1)

# add polygons into the Mark cell
cell_Mark2.add(gdspy.CellArray(cell_Mark1, 1, 1, (0, 0), (0, 0)))
cell_Mark2.add(L1_Tri1)

# create Top side Marks cell (with 3xMark1 and 1xMark2)
cell_Marks = gdspy.Cell('Marks')
cell_Marks.add(gdspy.CellArray(cell_Mark2, 1, 1, (0, 0), (-Shift2, Shift2)))
cell_Marks.add(gdspy.CellArray(cell_Mark1, 1, 1, (0, 0), (Shift2, Shift2),
                               rotation = 270))
cell_Marks.add(gdspy.CellArray(cell_Mark1, 1, 1, (0, 0), (Shift2, -Shift2),
                               rotation = 180))
cell_Marks.add(gdspy.CellArray(cell_Mark1, 1, 1, (0, 0), (-Shift2, -Shift2),
                               rotation = 90))


# Arrow
# -----
# Arrows to show the position of the central mark
cell_Arrow = gdspy.Cell('Arrow')
L1_Arrow = gdspy.Polygon([(-arrowS/2, 0), (0, 2*arrowS), (arrowS/2, 0)],
                          layer = 1)
cell_Arrow.add(L1_Arrow)

# Top
#----
cell_Top = gdspy.Cell('Top')
# add a circle representing a 4 inch wafer in the Top cell in layer 0
wafer = gdspy.Round((0, 0), 50000, number_of_points=64, layer=0)
cell_Top.add(wafer)
# add an array of Mark cell in the Top cell
cell_Top.add(gdspy.CellArray(cell_Marks, MarkN, MarkN,
                             (pitchX, pitchY),
                             (-pitchX*(MarkN-1)/2, -pitchY*(MarkN-1)/2)))
# add some arrows in the central part to show the position of the central mark
cell_Top.add(gdspy.CellArray(cell_Arrow, 1, 20, (0, 300), (0, -6300)))
cell_Top.add(gdspy.CellArray(cell_Arrow, 1, 20, (0, 300), (0, 6300),
                             rotation=180))

# write the coordinates of the alignment Mark in the Top cell
for i in range(0, MarkN):
    for j in range(0, MarkN):
        # layer 1
        textPosition = (-pitchX*(MarkN-1)/2 -120 + (i)*pitchX,
                        -pitchX*(MarkN-1)/2 + (j)*pitchY + 200)
        text = gdspy.Text((str(i)+','+str(j)), textS, textPosition, layer=1)
        cell_Top.add(text)

# write BS
text = gdspy.Text('TS', 2000, (-1500, 32000), layer=1)
cell_Top.add(text)
cell_Top.add(gdspy.CellArray(cell_Arrow, 2, 1, (6000, 0), (-3000, 32000), 
                             magnification = 20))


# Output
# ------
# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.write_gds('DWL66_TSCal_ManualMarks_200324.gds', 
                unit=1.0e-6, precision=1.0e-9)

