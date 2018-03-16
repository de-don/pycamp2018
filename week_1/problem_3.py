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
        slice: first slice or None
        slice: second slice or None

    """
    if isinstance(item, tuple):
        if len(item) == 1:
            return item[0], None
        elif len(item) == 2:
            return item
        else:
            raise TypeError('Slice must be int, slice, or tuple of them')
    else:
        if isinstance(item, slice) or isinstance(item, Integral):
            return item, None
        else:
            raise TypeError('Slice must be int, slice, or tuple of them')


class Matrix:
    """ Matrix class. Support many matrix-operations
    """
    rows = None
    n, m = 0, 0    # count rows and cols
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

        self.n = len(rows)
        self.m = max(map(len, rows), default=0)

        # checking dimension
        if self.m != min(map(len, rows), default=0):
            raise DimensionError

        self.rows = rows

    @property
    def size(self):
        """ Property which return size or matrix """
        return self.n, self.m

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
        return range(self.n)

    @property
    def range_m(self):
        """ Equal to range(self.m) """
        return range(self.m)

    @classmethod
    def zeros(cls, n, m):
        """ Create new Matrix n*m which contain from zeros

        Args:
            n(int): count rows
            m(int): count cols

        Returns:
            Matrix: matrix n*m from zeros
        """

        rows = [(0 for _ in range(m)) for _ in range(n)]
        return cls(*rows)

    @classmethod
    def ones(cls, n):
        """ Create new diag Matrix n*n with 1 by diag and 0 whatever else.

        Args:
            n(int): count rows and cols

        Returns:
            Matrix: E-matrix n*m
        """

        rows = [[i == j for j in range(n)] for i in range(n)]
        return cls(*rows)

    def __str__(self):
        s = f'[Matrix {self.n}x{self.m}]\n'
        s += repr(self)
        return s

    def __repr__(self):
        def len_fmt(x):
            return len(f'{x: ,.{self.precision}f}')

        max_len_in_col = []
        for i in self.range_m:
            q = 0
            for j in self.range_n:
                q = max(q, len_fmt(self.rows[j][i]) + (i != 0))
            max_len_in_col.append(q)

        lines = []
        for i in self.range_n:
            q = []
            for j in self.range_m:
                x = self.rows[i][j]
                q.append(f'{x:> #{max_len_in_col[j]},.{self.precision}f}')
            lines.append(''.join(q))
        return '\n'.join(map(str.rstrip, lines))

    def __getitem__(self, item):
        h, v = split_2d_slice(item)

        tmp = self.rows[:]
        if h is not None:
            if isinstance(h, Integral):
                tmp = [tmp[h]]
            elif isinstance(h, slice):
                tmp = tmp[h]

        if (v is not None) and tmp:
            if isinstance(v, Integral):
                tmp = [[row[v]] for row in tmp]
            elif isinstance(v, slice):
                tmp = [row[v] for row in tmp]

        matr = Matrix(*tmp)

        if matr.size == (1, 1):
            return matr.rows[0][0]

        if matr.n == 0 or matr.m == 0:
            return None

        return matr

    def __setitem__(self, key, value):
        h, v = split_2d_slice(key)

        if isinstance(value, Real) and isinstance(h, Integral) \
                and isinstance(v, Integral):
            self.rows[h][v] = value
        elif isinstance(value, Iterable) and isinstance(h, Integral) \
                and v is None:
            row = array('f', value)
            if len(row) != self.m:
                raise DimensionError

            self.rows[h] = array('f', value)
        else:
            raise TypeError


    ##################################################
    # Add methods
    ##################################################

    def __add__(self, other):
        tmp = self[:, :]
        tmp += other
        return tmp

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        """ Add matrix with equal sizes """
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise DimensionError

            for i in self.range_n:
                for j in self.range_m:
                    self.rows[i][j] += other.rows[i][j]

            return self
        else:
            raise TypeError('You can add/sub only Matrix to Matrix')

    ##################################################
    # sing methods
    ##################################################

    def __neg__(self):
        """ Return new matrix when: new_item = -old_item """
        tmp = self[:, :]
        for i in self.range_n:
            tmp.rows[i] = array('f', (-tmp.rows[i][j] for j in self.range_m))

        return tmp

    def __pos__(self):
        return self[:, :]

    ##################################################
    # Sub methods
    ##################################################

    def __sub__(self, other):
        tmp = self[:, :]
        tmp -= other
        return tmp

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
        tmp = self[:, :]
        tmp *= other
        return tmp

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
        tmp = self[:, :]
        tmp @= other
        return tmp

    def __imatmul__(self, other):
        """ Mul first matrix on second matrix by math rules. """
        if not isinstance(other, Matrix):
            raise TypeError

        if self.m != other.n:
            raise DimensionError

        tmp = [array('f', [0] * other.m) for _ in self.range_n]

        for i in self.range_n:
            for j in range(other.m):
                q = (self.rows[i][k] * other.rows[k][j] for k in self.range_m)
                tmp[i][j] = sum(q)

        self.rows = tmp
        self.m = other.m
        return self

    ##################################################
    # Pow methods
    ##################################################

    def __pow__(self, other):
        tmp = self[:, :]
        tmp **= other
        return tmp

    def __ipow__(self, other):
        """ Mul matrix on itself other times """
        if not isinstance(other, Integral):
            raise TypeError

        if self.n != self.m:
            raise DimensionError

        if other == 0:
            q = Matrix.ones(self.n)
            self.rows = q.rows
        elif other > 1:
            q = self[:, :]
            for i in range(other - 1):
                self @= q
        return self
