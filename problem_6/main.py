from collections import OrderedDict


class Series:
    def __init__(self, row, col_names):
        row = list(map(self.detect_type, row))
        col_names = list(col_names)
        if len(row) != len(col_names):
            ValueError("Len(row) != Len(col_names)")

        self._items = OrderedDict(zip(col_names, row))

    @staticmethod
    def detect_type(item):
        types = (int, float)
        for cur_type in types:
            try:
                new_item = cur_type(item)
                if str(new_item) == item:
                    return new_item
            except ValueError:
                pass
        return item


    def __getitem__(self, item):
        return self._items[item]

    def __str__(self):
        s = []
        for title, value in self._items.items():
            s.append(f'{title}: {value}')
        return "\n".join(s)


class Table:
    def __init__(self, rows, col_names=None):
        rows = list(rows)
        self.rows_count = len(rows)
        self.cols_count = len(rows[0]) if self.rows_count else 0

        if not col_names:
            self.col_names = [f'col_{i}' for i in range(self.cols_count)]
        self.col_names = list(col_names)

        self.rows = [Series(row, self.col_names) for row in rows]

    def __str__(self):
        s = []
        for row_num, row in enumerate(self.rows):
            s.append(f'{row_num}:')
            for title in self.col_names:
                value = row[title]
                s.append(f'    {title}: {value}')
        return "\n".join(s)

    @classmethod
    def from_csv(cls, file_path):
        with open(file_path, 'r') as file:
            try:
                head = next(file).rstrip().split(";")
            except StopIteration:
                raise Exception('Head not found')

            lines = (line.rstrip().split(";") for line in file)

            return cls(rows=lines, col_names=head)

    def filter(self, **kwargs):
        pass

    def count(self):
        return self.rows_count

    def sum(self, col_name):
        return sum(row[col_name] for row in self.rows)

    def avg(self, col_name):
        return self.sum(col_name) / self.rows_count

    def unique(self, col_name):
        return set(row[col_name] for row in self.rows)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Index must be integer.")

        return self.rows[item]

    def columns(self, *col_names):
        pass

    @property
    def headers(self):
        return self.col_names[:]

    def order_by(self, col_name, reversed=False):
        pass


if __name__ == '__main__':
    data = Table.from_csv('input.csv')
    print(data)
