import datetime
import operator
from collections import OrderedDict
from operator import itemgetter


class NotSupported(ValueError):
    """ Error raise which function not supported """
    pass


class Series:
    def __init__(self, row, col_names):
        row = list(map(self.detect_type, list(row)))
        col_names = list(col_names)
        if len(row) != len(col_names):
            ValueError("Len(row) != Len(col_names)")

        self._items = OrderedDict(zip(col_names, row))

    @staticmethod
    def detect_type(item):
        """ Detect type of item, int, float or date """
        types = (
            int,
            float,
            lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'),
            lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d')
        )

        # check each type
        for cur_type in types:
            try:
                new_item = cur_type(item)
                return new_item
            except (ValueError, TypeError):
                pass
        # if type not be found, leave str type
        return item

    def __getitem__(self, item):
        return self._items[item]

    def __str__(self):
        lines = (f'{title}: {value}' for title, value in self._items.items())
        return "\n".join(lines)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Objects have different types")
        return self._items == other._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.items())


class Table:
    SUPPORTED_FUNCS = {
        str: ['startswith', 'endswith'],
        int: ['gt', 'lt', 'ge', 'le'],
        datetime.datetime: ['gt', 'lt', 'ge', 'le'],
    }

    def __init__(self, rows, col_names):
        self.col_names = list(col_names)
        self.cols_count = len(self.col_names)

        self.rows = [Series(row, self.col_names) for row in rows]
        self.rows_count = len(self.rows)

    def __str__(self):
        if not self.rows_count:
            return "None"

        lines = []
        for row_num, row in enumerate(self.rows):
            lines.append(f'{row_num}:')
            lines.extend('    ' + line for line in str(row).splitlines())
        return "\n".join(lines)

    __repr__ = __str__

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
        params = key.split("__", 1)
        if len(params) == 2:
            return params
        return params[0], None

    def filter(self, **kwargs):
        data = self.copy()
        rows = data.rows
        for key, value in kwargs.items():
            key, func = self.split_key_filtering(key)

            if func is None:
                # if it is simple filtering without function
                def filter_func(x):
                    return x[key] == value

                rows = filter(filter_func, rows)
                continue

            # if function exists, check type on supporting
            key_type = type(rows[0][key])
            if key_type not in self.SUPPORTED_FUNCS:
                raise NotSupported("Type not supported")

            # and check function on supporting
            if func not in self.SUPPORTED_FUNCS[key_type]:
                raise NotSupported(
                    f"Function {func} not supported for {key_type.__name__}"
                )

            # if function not found for type, find it in operator
            if not getattr(key_type, func, None):
                key_type = operator

            # create function for filter
            def filter_func(x):
                return getattr(key_type, func)(x[key], value)

            rows = filter(filter_func, rows)

        # create list from filters and save it's
        data.rows = list(rows)
        data.rows_count = len(data.rows)
        return data

    def count(self):
        return self.rows_count

    def sum(self, col_name):
        return sum(row[col_name] for row in self.rows)

    def avg(self, col_name):
        return self.sum(col_name) / self.rows_count if self.rows_count else 0

    def unique(self, col_name):
        return set(row[col_name] for row in self.rows)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Index must be integer.")
        return self.rows[item]

    def columns(self, *col_names):
        new_rows = (
            (row[col_name] for col_name in col_names)
            for row in self.rows
        )
        return Table(new_rows, col_names)

    @property
    def headers(self):
        return self.col_names[:]

    def order_by(self, col_name, reversed=False):
        new_table = self.copy()
        new_table.rows.sort(key=itemgetter(col_name), reverse=reversed)
        return new_table

    def copy(self):
        rows = (
            map(itemgetter(1), row)
            for row in self.rows
        )
        return Table(rows, col_names=self.col_names)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Not same types to compare")
        return self.rows == other.rows and self.col_names == self.col_names
