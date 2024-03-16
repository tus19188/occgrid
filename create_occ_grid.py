import math
import numpy as np
import map_conversions as mc

def create_occupancy_grid(boundary, blocks, res):
    # create_occupancy_grid creates an occupancy grid array representing the
    # environment described by the inputs
    #
    # inputs:
    # boundary array with [xmin, ymin, xmax, ymax]
    # blocks array of arrays with [[xmin, ymin, xmax, ymax], ...] for each block
    # res cell size
    # outputs:
    # numpy array containing the occupancy values in row-major order
    # Note: empty cells should have a value of 0 and occupied cells should
    # have a value of 100
    # Note: the lower left corner is the first cell
    
    ##### YOUR CODE STARTS HERE #####
    # calculate the number of rows and columns in the grid
    num_rows = int(math.ceil((boundary[3] - boundary[1]) / res))
    num_cols = int(math.ceil((boundary[2] - boundary[0]) / res))
    
    # initialize the occupancy grid with zeros (empty cells)
    occupancy_grid = np.zeros((num_rows, num_cols), dtype=int)
    
    # iterate through each block and mark the corresponding cells as occupied
    for block in blocks:
        xmin, ymin, xmax, ymax = block
        # convert block coordinates to row and column indices
        block_rows, block_cols = mc.xy2sub(boundary, res, np.array([xmin, xmax]),
                                            np.array([ymin, ymax]))
        # ensure block indices are within grid bounds
        block_rows = np.clip(block_rows, 0, num_rows - 1)
        block_cols = np.clip(block_cols, 0, num_cols - 1)
        
        # mark cells within the block as occupied
        occupancy_grid[block_rows[0]:block_rows[1]+1, block_cols[0]:block_cols[1]+1] = 100
                    
    return occupancy_grid
    ##### YOUR CODE ENDS HERE #####