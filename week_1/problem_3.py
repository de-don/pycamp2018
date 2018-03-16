from array import array
from itertools import chain
from numbers import Integral, Real


class DimensionError(ValueError):
    pass


def split_2d_slice(item):
    if isinstance(item, tuple):
        if len(item) == 1:
            return item[0], None
        elif len(item) == 2:
            return item
        else:
            raise TypeError("Slice must be int, slice, or tuple of them")
    else:
        if isinstance(item, slice) or isinstance(item, Integral):
            return item, None
        else:
            raise TypeError("Slice must be int, slice, or tuple of them")


class Matrix:
    rows = None
    n, m = 0, 0  # count rows and cols
    width = 5

    def __init__(self, *args):
        rows = [array('f', row) for row in args]

        self.n = len(rows)
        self.m = max(map(len, rows), default=0)

        # checking dimension
        if self.m != min(map(len, rows), default=0):
            raise DimensionError

        self.rows = rows
        self.calc_width()

    def calc_width(self):
        """ Method to calc column width """
        self.width = max(map(len, map(str, chain.from_iterable(self.rows))), default=0) + 1

    @property
    def size(self):
        return self.n, self.m

    @property
    def T(self):
        tmp = [[self.rows[j][i] for j in range(self.n)] for i in range(self.m)]
        return Matrix(*tmp)

    def __str__(self):
        s = f'Matrix {self.n}x{self.m}\n'
        s += '=' * (self.width * self.m - 1) + '\n'
        s += repr(self)
        return s

    def __repr__(self):
        lines = []
        for row in self.rows:
            lines.append(''.join(f'{i:<{self.width}}' for i in row))
        return '\n'.join(map(str.strip, lines))

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
        # not completed!!!

        h, v = split_2d_slice(key)

        if isinstance(value, Real):
            if isinstance(h, Integral) and isinstance(v, Integral):
                self.rows[h][v] = value
            else:
                raise TypeError
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
        if isinstance(other, Matrix):
            if self.size != other.size:
                raise DimensionError

            for i in range(self.n):
                for j in range(self.m):
                    self.rows[i][j] += other.rows[i][j]
            self.calc_width()
            return self
        else:
            raise TypeError("You can add/sub only Matrix to Matrix")

    ##################################################
    # sing methods
    ##################################################

    def __neg__(self):
        tmp = self[:, :]
        for i in range(self.n):
            tmp.rows[i] = array('f', (-tmp.rows[i][j] for j in range(self.m)))
        tmp.calc_width()

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
        return all((self.rows[i] == other.rows[i] for i in range(self.n)))

    ##################################################
    # Mul methods
    ##################################################

    def __mul__(self, other):
        tmp = self[:, :]
        tmp *= other
        return tmp

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        if not isinstance(other, Real):
            raise TypeError

        self.rows = [[item * other for item in row] for row in self.rows]
        self.calc_width()
        return self

    ##################################################
    # MatMul
    ##################################################

    def __matmul__(self, other):
        tmp = self[:, :]
        tmp @= other
        return tmp

    def __imatmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError

        if self.m != other.n:
            raise DimensionError

        tmp = [array('f', [0] * other.m) for _ in range(self.n)]

        for i in range(self.n):
            for j in range(other.m):
                q = (self.rows[i][k] * other.rows[k][j] for k in range(self.m))
                tmp[i][j] = sum(q)

        self.rows = tmp
        self.calc_width()
        return self

    ##################################################
    # Pow methods
    ##################################################

    def __pow__(self, other):
        tmp = self[:, :]
        tmp **= other
        return tmp

    def __ipow__(self, other):
        if not isinstance(other, Integral):
            raise TypeError

        if self.n != self.m:
            raise DimensionError

        q = self[:, :]
        for i in range(other - 1):
            self @= q
        return self
