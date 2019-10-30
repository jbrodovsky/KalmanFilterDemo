import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        #print('Calculating the determinant')
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        if self.h == 1:
            return self.g[0][0]
        elif self.h == 2:
            return self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0]
        else:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        # TODO - your code here

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        #print('Calculating the trace')
        trc = []
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        # TODO - your code here
        else:
            for i in range(self.h):
                trc.append(self.g[i][i])
        return (sum(trc))

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        # TODO - your code here
        if self.h == 1:
            return Matrix([[1/self.g[0][0]]])            
        else:            
            return 1/self.determinant() * (self.trace() * identity(2) - self)
            
    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        #print('Calculating the transpose')
        # TODO - your code here
        t = []
        for c in range(self.w):
            row = []
            for r in range(self.h):
                row.append(self.g[r][c])
            t.append(row)
        return Matrix(t)

    def is_square(self):
        return self.h == self.w
    
    def get_row(self, row):
        return self.g[row]
    
    def get_col(self, col):
        column = []
        for r in range(len(self.g)):
            column.append(self.g[r][col])
        return column
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        new_matrix = zeroes(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                new_matrix[i][j] = self.g[i][j] + other.g[i][j]
        return new_matrix

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        if self.h != 0 and self.w != 0:
            new_matrix = zeroes(self.h, self.w)
            for i in range(self.h):
                for j in range(self.w):
                    new_matrix[i][j] = -self.g[i][j]
            return new_matrix
        else:
            raise(ValueError, "Matrix must have values to negate") 

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
        new_matrix = zeroes(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                new_matrix[i][j] = self.g[i][j] - other.g[i][j]
        return new_matrix

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #print('Matrix 1: ')
        #print(self)
        #print('Matrix 2:')
        #print(other)
        if self.w == other.h:
            m = []
            #print('Matrix dimensions match')
            for r in range(len(self.g)):
                row = self.get_row(r)
                newRow = []
                for c in range(len(other.g[0])):
                    col = other.get_col(c)
                    #print('Multiplying row #',r,' with col #',c,' -> ',row,' * ', col)
                    num = 0
                    for i in range(len(col)):
                        #print('\tMultiplying item #',i,':',row[i],'*',col[i],'=',row[i] * col[i])
                        num += row[i] * col[i]
                    newRow.append(num)
                m.append(newRow)
            #print(m)
            newMatrix = Matrix(m)
            #print(newMatrix.T())
            return newMatrix
            #return Matrix(m)
        else:
            raise(ValueError, "Matrix dimensions do not agree")

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            for i in range(self.h):
                for j in range(self.w):
                    self[i][j] = self[i][j] * other
            return self
            