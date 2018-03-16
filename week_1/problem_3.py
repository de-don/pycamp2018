from array import array
from itertools import chain


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
            raise Exception("len each of rows must be equal")

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
        return '\n'.join(lines)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) == 1:
                h, v = item[0], None
            elif len(item) == 2:
                h, v = item
            else:
                raise TypeError("Slice must be int, slice, or tuple of them")
        else:
            h, v = item, None

        tmp = self.rows[:]
        if h is not None:
            if isinstance(h, int):
                tmp = [tmp[h]]
            elif isinstance(h, slice):
                tmp = tmp[h]

        if (v is not None) and tmp:
            if isinstance(v, int):
                tmp = [[row[v]] for row in tmp]
            elif isinstance(v, slice):
                tmp = [row[v] for row in tmp]

        matr = Matrix(*tmp)

        if matr.size == (1, 1):
            return matr.rows[0][0]

        if matr.n == 0 or matr.m == 0:
            return None

        return matr


if __name__ == "__main__":
    m = Matrix((1, 2, 3,), (4, 5, 6), (7, 8, 9), (10, 11, 12))

    print(m[1:1])
