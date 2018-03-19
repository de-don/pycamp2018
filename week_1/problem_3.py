from array import array
from collections import Iterable
from numbers import Integral, Real


class DimensionError(ValueError):
    """ Error raiser when dimensions two items not equal """
    pass


def split_2d_slice(item):
    """ Function to split 2d slice

    Args:
        item(Tuple[slice]): pair of slice or int.

    Returns:
        1) slice: first slice or None
        2) slice: second slice or None

    """
    if isinstance(item, tuple):
        if len(item) == 1:
            return item[0], None
        elif len(item) == 2:
            return item
        else:
            raise TypeError('Ltn of tuple for slice must be 1 or 2!')
    else:
        return item, None


class Matrix:
    """ Matrix class. Support many matrix-operations """
    rows = None
    count_rows, count_cols = 0, 0  # count rows and cols
    precision = 1  # precision for output

    def __init__(self, *args, precision=1):
        """ Init function which create matrix from args.

        Args:
            *args(Iterable): iter of iterable objects, every object must
                be number (float or int)
            precision(int): precision for printing.

        Returns:
            NoneType: return nothing

        """

        self.precision = precision
        rows = [array('f', row) for row in args]

        self.count_rows = len(rows)
        self.count_cols = max(map(len, rows), default=0)

        # checking dimension
        if self.count_cols != min(map(len, rows), default=0):
            raise DimensionError

        self.rows = rows

    @property
    def size(self):
        """ Property which return size or matrix """
        return self.count_rows, self.count_cols

    @property
    def T(self):
        """ Property for create transpose matrix and return it

        Return:
            Matrix: transposed matrix
        """

        tmp = [[self.rows[j][i] for j in self.range_n] for i in self.range_m]
        return Matrix(*tmp)

    @property
    def range_n(self):
        """ Equal to range(self.n) """
        return range(self.count_rows)

    @property
    def range_m(self):
        """ Equal to range(self.m) """
        return range(self.count_cols)

    @classmethod
    def zeros(cls, count_rows, count_cols):
        """ Create new Matrix n*m which contain from zeros

        Args:
            count_rows(int): count rows
            count_cols(int): count cols

        Returns:
            Matrix: matrix n*m from zeros
        """

        rows = [(0 for _ in range(count_cols)) for _ in range(count_rows)]
        return cls(*rows)

    @classmethod
    def ones(cls, count_rows):
        """ Create new diag Matrix n*n with 1 by diag and 0 whatever else.

        Args:
            count_rows(int): count rows and cols

        Returns:
            Matrix: E-matrix n*m
        """

        rows = [[i == j for j in range(count_rows)] for i in range(count_rows)]
        return cls(*rows)

    def __str__(self):
        text = f'[Matrix {self.count_rows}x{self.count_cols}]\n'
        text += repr(self)
        return text

    def __repr__(self):
        def len_fmt(x):
            return len(f'{x: ,.{self.precision}f}')

        # calculate maximum len in each column.
        max_len_in_col = []
        for num_col in self.range_m:
            max_len = 0
            for num_row in self.range_n:
                # calc len current cell and compare it with max_len
                current_len = len_fmt(self.rows[num_row][num_col])
                max_len = max(max_len, current_len + (num_col != 0))

            max_len_in_col.append(max_len)

        # create lines of matrix
        lines = []
        for num_row in self.range_n:
            cells = []
            for num_col in self.range_m:
                cell = self.rows[num_row][num_col]
                width = max_len_in_col[num_col]
                cells.append(f'{cell:> #{width},.{self.precision}f}')
            lines.append(''.join(cells))

        return '\n'.join(map(str.rstrip, lines))

    def __getitem__(self, item):
        # get horizontal and vertical slices
        h_slice, v_slice = split_2d_slice(item)

        tmp_matrix = list(self)

        # horizontal slice, if exists
        if h_slice is not None:
            if isinstance(h_slice, Integral):
                tmp_matrix = [tmp_matrix[h_slice]]
            elif isinstance(h_slice, slice):
                tmp_matrix = tmp_matrix[h_slice]
            else:
                raise TypeError('Slice must be int, slice, or tuple of them')

        # vertical slice, if exists
        if (v_slice is not None) and tmp_matrix:
            if isinstance(v_slice, Integral):
                tmp_matrix = [[row[v_slice]] for row in tmp_matrix]
            elif isinstance(v_slice, slice):
                tmp_matrix = [row[v_slice] for row in tmp_matrix]
            else:
                raise TypeError('Slice must be int, slice, or tuple of them')

        # create matrix from slice
        matr = Matrix(*tmp_matrix)

        # If need return one number
        if isinstance(h_slice, Integral) and isinstance(v_slice, Integral):
            if matr.size == (1, 1):
                return matr.rows[0][0]

        if matr.count_rows == 0 or matr.count_cols == 0:
            return None

        return matr

    def __setitem__(self, key, value):
        h_slice, v_slice = split_2d_slice(key)

        if isinstance(value, Real) and isinstance(h_slice, Integral) \
                and isinstance(v_slice, Integral):
            self.rows[h_slice][v_slice] = value
        elif isinstance(value, Iterable) and isinstance(h_slice, Integral) \
                and v_slice is None:
            row = array('f', value)
            if len(row) != self.count_cols:
                raise DimensionError

            self.rows[h_slice] = array('f', value)
        else:
            raise TypeError

    def __iter__(self):
        return (list(row) for row in self.rows)

    ##################################################
    # Add methods
    ##################################################

    def __add__(self, other):
        tmp_matrix = self[:, :]
        tmp_matrix += other
        return tmp_matrix

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        """ Add matrix with equal sizes """
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise DimensionError

            for num_row in self.range_n:
                for num_col in self.range_m:
                    self.rows[num_row][num_col] += other.rows[num_row][num_col]

            return self
        else:
            raise TypeError('You can add/sub only Matrix to Matrix')

    ##################################################
    # sing methods
    ##################################################

    def __neg__(self):
        """ Return new matrix when: new_item = -old_item """
        tmp_matrix = self[:, :]
        for i in self.range_n:
            tmp_matrix.rows[i] = array('f', (-tmp_matrix.rows[i][j] for j in self.range_m))

        return tmp_matrix

    def __pos__(self):
        return self[:, :]

    ##################################################
    # Sub methods
    ##################################################

    def __sub__(self, other):
        tmp_matrix = self[:, :]
        tmp_matrix -= other
        return tmp_matrix

    def __rsub__(self, other):
        return (-self) + other

    def __isub__(self, other):
        self += (-other)
        return self

    ##################################################
    # Comparison methods
    ##################################################

    def __eq__(self, other):
        """ Compare matrix. Two matrix is equal if equal each item's pair """
        return all((self.rows[i] == other.rows[i] for i in self.range_n))

    ##################################################
    # Mul methods
    ##################################################

    def __mul__(self, other):
        """ Mul matrix on number

        Args:
            other(Real): number to multiplicate

        Returns:
            Matrix: return new Matrix

        """
        tmp_matrix = self[:, :]
        tmp_matrix *= other
        return tmp_matrix

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        """ Mul matrix on number

        Args:
            other(Real): number to multiplicate

        Returns:
            Matrix: return self

        """
        if not isinstance(other, Real):
            raise TypeError

        self.rows = [[item * other for item in row] for row in self.rows]
        return self

    ##################################################
    # MatMul
    ##################################################

    def __matmul__(self, other):
        tmp_matrix = self[:, :]
        tmp_matrix @= other
        return tmp_matrix

    def __imatmul__(self, other):
        """ Mul first matrix on second matrix by math rules. """
        if not isinstance(other, Matrix):
            raise TypeError

        if self.count_cols != other.count_rows:
            raise DimensionError

        tmp_rows = [array('f', [0] * other.count_cols) for _ in self.range_n]

        for i in self.range_n:
            for j in range(other.count_cols):
                q = (self.rows[i][k] * other.rows[k][j] for k in self.range_m)
                tmp_rows[i][j] = sum(q)

        self.rows = tmp_rows
        self.count_cols = other.count_cols
        return self

    ##################################################
    # Pow methods
    ##################################################

    def __pow__(self, other):
        tmp_matrix = self[:, :]
        tmp_matrix **= other
        return tmp_matrix

    def __ipow__(self, other):
        """ Mul matrix on itself other times """
        if not isinstance(other, Integral):
            raise TypeError

        if self.count_rows != self.count_cols:
            raise DimensionError

        if other == 0:
            q = Matrix.ones(self.count_rows)
            self.rows = q.rows
        elif other > 1:
            q = self[:, :]
            for i in range(other - 1):
                self @= q
        return self
