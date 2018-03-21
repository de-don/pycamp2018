from collections import OrderedDict
import operator
from operator import itemgetter
import datetime

class NotSupported(ValueError):
    pass

class Series:
    def __init__(self, row, col_names):
        row = list(map(self.detect_type, row))
        col_names = list(col_names)
        if len(row) != len(col_names):
            ValueError("Len(row) != Len(col_names)")

        self._items = OrderedDict(zip(col_names, row))

    @staticmethod
    def detect_type(item):
        # date format: 2018-03-20 18:30:30
        date_time = lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')
        date = lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d')

        types = (int, float, date_time, date)
        for cur_type in types:
            try:
                new_item = cur_type(item)
                return new_item
            except (ValueError, TypeError):
                pass
        return item

    def __getitem__(self, item):
        return self._items[item]

    def __str__(self):
        s = []
        for title, value in self._items.items():
            s.append(f'{title}: {value}')
        return "\n".join(s)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Not same types to compare")
        return self._items == other._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.items())


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
        if not self.rows_count:
            return "None"

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

    @staticmethod
    def split_key_filtering(key):
        params = key.split("__")
        if len(params) > 2:
            raise KeyError("Sub-filtering not supported")
        if len(params) == 2:
            return params
        return params[0], None

    def filter(self, **kwargs):
        supported_funcs = {
            str: ['startswith', 'endswith'],
            int: ['gt', 'lt', 'ge', 'le'],
            datetime.datetime: ['gt', 'lt', 'ge', 'le'],
        }

        data = self.copy()
        rows = data.rows
        for key, value in kwargs.items():
            key, func = self.split_key_filtering(key)
            filter_func = None

            if func is None:
                filter_func = lambda x: x[key] == value
                rows = list(filter(filter_func, rows))
                continue

            key_type = type(rows[0][key])
            if not key_type in supported_funcs:
                raise NotSupported("Type not supported")

            if func not in supported_funcs[key_type]:
                raise NotSupported(f"Function {func} not supported"
                                          f" for {key_type.__name__}")

            if getattr(key_type, func, None):
                filter_func = lambda x: getattr(key_type, func)(x[key], value)
            else:
                filter_func = lambda x: getattr(operator, func)(x[key], value)

            rows = list(filter(filter_func, rows))

        data.rows = rows
        data.rows_count = len(rows)
        return data

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
        new_rows = []
        for row in self.rows:
            new_row = []
            for col_name in col_names:
                new_row.append(row[col_name])
            new_rows.append(new_row)
        return Table(new_rows, col_names)

    @property
    def headers(self):
        return self.col_names[:]

    def order_by(self, col_name, reversed=False):
        new_table = self.copy()
        new_table.rows.sort(key=itemgetter(col_name), reverse=reversed)

        return new_table

    def copy(self):
        rows = (list(map(itemgetter(1), row)) for row in self.rows)
        return Table(rows, col_names=self.col_names)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Not same types to compare")
        return self.rows == other.rows and self.col_names == self.col_names


if __name__ == '__main__':
    data = Table.from_csv('input.csv')
    print(data)
