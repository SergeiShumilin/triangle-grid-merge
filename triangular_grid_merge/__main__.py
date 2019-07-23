from grid import Grid
from tecplot import read_tecplot
from tecplot import print_tecplot

# grid = Grid()
# grid.init(4, 5, (0, 60), (0, 100))
# print_tecplot(grid, 'grid.dat')

#read_multizone_tecplot(grid, 'grid.dat')
#print_merged_grid_tecplot(grid, 'merged_grid.dat')
#print_multizone_tecplot(grid, 'double_grid.dat')
if __name__ == '__main__':
    grid = Grid()
    read_tecplot(grid, 'double_grid.dat')

    print_tecplot(grid, 'threezones.dat', merge=True)





