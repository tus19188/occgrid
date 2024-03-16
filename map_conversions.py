import numpy as np

def sub2ind(array_shape, rows, cols):
    # sub2ind coverts subscript (row, column) pairs into linear indices in
    # row-major order
    #
    # inputs:
    #   array_shape array with [# of rows, # of columns]
    #   rows        numpy array of row indices
    #   cols        numpy array of column indices
    # outputs:
    #   numpy array of integer indices
    #       Note: (row, column) pairs that are not valid should have a 
    #       corresponding output index of -1
    
    ind = rows * array_shape[1] + cols
    inv_ind = (rows < 0) | (rows >= array_shape[0]) | (cols < 0) | (cols >= array_shape[1])
    ind[inv_ind] = -1
    return ind

def ind2sub(array_shape, ind):
    # ind2sub converts linear indices in a row-major array to subscript
    # (row, column) pairs
    #
    # inputs:
    #   array_shape array with [# of rows, # of columns]
    #   ind         numpy array of integer indices
    # outputs:
    #   numpy array of row indices
    #   numpy array of column indices
    #       Note: any indices that are not valid should have row and column
    #       subscripts outputs of -1
    
    rows = ind // array_shape[1]
    cols = ind % array_shape[1]
    inv_ind = (ind < 0) | (rows >= array_shape[0]) | (cols < 0) | (cols >= array_shape[1])
    rows[inv_ind] = -1
    cols[inv_ind] = -1
    return rows, cols
    
def xy2sub(boundary, res, x, y):
    # xy2sub converts (x,y) coordinate pairs into (row, column) subscript pairs
    #
    # inputs:
    #   boundary    array with [xmin, ymin, xmax, ymax]
    #   res         cell size
    #   x           numpy array of x values
    #   y           numpy array of y values
    # outputs:
    #   numpy array of row indices
    #   numpy array of column indices
    #       Note: any (x,y) pairs that are not valid should have subscript
    #       outputs of -1
    
    rows = np.floor((y - boundary[1]) / res).astype(int)
    cols = np.floor((x - boundary[0]) / res).astype(int)
    
    # Check for points on top right of boundary
    rows[y == boundary[3]] = int((boundary[3] - boundary[1]) / res) - 1
    cols[x == boundary[2]] = int((boundary[2] - boundary[0]) / res) - 1

    # Handle points outside the boundary and nan points
    inv_ind = (x < boundary[0]) | (x > boundary[2]) | (y < boundary[1]) | (y > boundary[3]) | np.isnan(x) | np.isnan(y)
    rows[inv_ind] = -1
    cols[inv_ind] = -1
  
    return rows, cols

def sub2xy(boundary, res, rows, cols):
    # sub2xy converts (row, column) subscript pairs into (x,y) coordinate pairs
    #
    # inputs:
    #   boundary    array with [xmin, ymin, xmax, ymax]
    #   res         cell size
    #   rows        numpy array of row indices
    #   cols        numpy array of column indices
    # outputs:
    #   numpy array of x coordinates of center of each cell
    #   numpy array of y coordinates of center of each cell
    #       Note: any (row, col) pairs that are not valid should have outputs
    #       of numpy NaN
    
    x = boundary[0] + res * (cols + 0.5)
    y = boundary[1] + res * (rows + 0.5)
    inv_ind = (x < boundary[0]) | (x > boundary[2]) | (y < boundary[1]) | (y > boundary[3])
    x[inv_ind] = np.NaN
    y[inv_ind] = np.NaN
    return x, y

def xy2ind(boundary, res, array_shape, x, y):
    # xy2ind converts (x,y) coordinate pairs into linear indices in row-major
    # order
    #
    # inputs:
    #   boundary    array with [xmin, ymin, xmax, ymax]
    #   res         cell size
    #   array_shape numpy array with [# of rows, # of columns]
    #   x           numpy array of x values
    #   y           numpy array of y values
    # outputs:
    #   numpy array of row indices
    #   numpy array of column indices
    
    rows, cols = xy2sub(boundary, res, x, y)
    ind = sub2ind(array_shape, rows, cols)
    return ind

def ind2xy(boundary, res, array_shape, ind):
    # ind2xy converts linear indices in row-major order into (x,y) coordinate
    # pairs
    #
    # inputs:
    #   boundary    array with [xmin, ymin, xmax, ymax]
    #   res         cell size
    #   array_shape numpy array with [# of rows, # of columns]
    #   ind         numpy array of indices
    # outputs:
    #   numpy array of x coordinates
    #   numpy array of y coordinates
    
    rows, cols = ind2sub(array_shape, ind)
    x, y = sub2xy(boundary, res, rows, cols)
    return x, y