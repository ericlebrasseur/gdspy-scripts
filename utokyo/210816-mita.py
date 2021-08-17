import gdspy

lib = gdspy.GdsLibrary()

# Geometry must be placed in cells.
inv_cell = lib.new_cell('inv')

# Load a GDSII file into a new library
lib.read_gds('utokyo/210816-mita.gds')
inv = gdspy.boolean(lib.cells['frame'], lib.cells['top'], "not")
inv_cell.add(inv)

# Save the library in a file called 'first.gds'.
lib.write_gds('utokyo/210816-mita-inv.gds')

# Display all cells using the internal viewer.
# gdspy.LayoutViewer()