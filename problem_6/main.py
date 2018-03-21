import csv
import datetime
import json
import operator
import sqlite3
from collections import OrderedDict
from functools import partial
from operator import itemgetter


class NotSupported(ValueError):
    """ Error raise which function not supported """
    pass


class Entry:
    """ Class for storing one table row. """

    # supported types and their functions for filtering
    SUPPORTED_FUNCS = {
        str: ['startswith', 'endswith'],
        int: ['gt', 'lt', 'ge', 'le'],
        datetime.datetime: ['gt', 'lt', 'ge', 'le'],
    }

    def __init__(self, row, col_names):
        """
        Args:
            row(Iterable): iterator of items.
            col_names(Iterable): iterator of strings.
        """

        col_names = list(col_names)
        if len(set(col_names)) < len(col_names):
            raise ValueError("Names of columns must be unique")

        # detection type of each element
        row = list(map(self.detect_type, list(row)))

        if len(row) != len(col_names):
            raise ValueError("Len(row) != Len(col_names)")

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

    def _check(self, key, value, func=None):
        cell_value = self[key]
        if func is None:
            # if it is simple filtering without function
            return cell_value == value

        key_type = cell_value.__class__
        # and check function on supporting
        if func not in self.SUPPORTED_FUNCS.get(key_type, []):
            raise NotSupported(f"{func} not supported for {key_type.__name__}")

        # if function not found for type, find it in operator
        if not getattr(key_type, func, None):
            key_type = operator
        return getattr(key_type, func)(cell_value, value)


class Table:
    """ Class for easy working with tables. """

    def __init__(self, rows, col_names):
        """
        Args:
            row(Iterable): iterator of iterators. For example [[1, 2], [3, 4]].
            col_names(Iterable): iterator of strings.
        """
        self.col_names = list(col_names)

        self.rows = [Entry(row, self.col_names) for row in rows]

    def __str__(self):
        if not self.rows_count:
            return "Empty"

        lines = []
        for row_num, row in enumerate(self.rows):
            lines.append(f'{row_num}:')
            lines.extend('    ' + line for line in str(row).splitlines())
        return "\n".join(lines)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Not same types to compare")
        return self.rows == other.rows and self.col_names == self.col_names

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Index must be integer.")
        return self.rows[item]

    ##################################################
    # load methods
    ##################################################

    @classmethod
    def from_csv(cls, file_path, delimiter=";"):
        """ Load Table from csv file.

        Args:
            file_path(str): path to csv file.
            delimiter(str): csv delimiter.

        Returns:
            Table: Table created from data of the file.
        """
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            head = next(reader)
            lines = reader
            return cls(rows=lines, col_names=head)

    @classmethod
    def from_json(cls, file_path):
        """ Load Table from json file.

        Args:
            file_path(str): path to json file.

        Returns:
            Table: Table created from data of the file.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
            head = list(data.keys())
            columns = data.values()
            rows_count = len(data[head[0]])
            lines = (
                (column[i] for column in columns)
                for i in range(rows_count)
            )
            return cls(rows=lines, col_names=head)

    @classmethod
    def from_sqlite3(cls, file_path, table_name):
        """ Load Table from sqlite3 database file.

        Args:
            file_path(str): path to sqlite3 file.

        Returns:
            Table: Table created from data of the database.
        """
        with sqlite3.connect(file_path) as con:
            data = con.execute(f'PRAGMA table_info({table_name});')
            head = (row[1] for row in data)
            lines = con.execute(f'SELECT * FROM {table_name};')
            return cls(rows=lines, col_names=head)

    ##################################################
    # export methods
    ##################################################

    def to_csv(self):
        pass

    def to_json(self):
        pass

    def to_html(self):
        pass

    ##################################################
    # other methods
    ##################################################

    @staticmethod
    def split_key_filtering(key):
        """ Split key such as 'date__gt' by '__' and return parts.

        if '__' not in key, return key and None.

        Args:
            key(str): keyword with '__' or not

        Returns:
            str: first part of key
            str or None: second part of key
        """
        params = key.split("__", 1)
        if len(params) == 2:
            return params
        return params[0], None

    def filter(self, **kwargs):
        """ Filtering table by columns or by functions of columns.

        Each item from kwargs must belong one of next patterns:
            {key}__{function} = {value},
            {key} = {value}.
        Supported functions for current type stored in SUPPORTED_FUNCS

        If function not supported, raise NotSupported
        """

        data = self.copy()
        rows = data.rows
        for key, value in kwargs.items():
            key, func = self.split_key_filtering(key)

            filter_func = partial(
                Entry._check,
                key=key,
                value=value,
                func=func
            )
            rows = filter(filter_func, rows)

        # create list from filters and save it's
        data.rows = list(rows)
        return data

    def count(self):
        """ Function return count of rows """
        return self.rows_count

    def sum(self, col_name):
        """ Sum of column with name 'col_name' """
        return sum(row[col_name] for row in self.rows)

    def avg(self, col_name):
        """ Avg of column with name 'col_name' """
        return self.sum(col_name) / self.rows_count if self.rows_count else 0

    def unique(self, col_name):
        """ Unique values of column with name 'col_name'

        Returns:
            set: Unique values stored in col_name
        """
        return set(row[col_name] for row in self.rows)

    def columns(self, *col_names):
        """ Create new Table which contain only columns from 'col_names'. """
        new_rows = (
            (row[col_name] for col_name in col_names)
            for row in self.rows
        )
        return Table(new_rows, col_names)

    def order_by(self, col_name, reversed=False):
        """ Return new Table which rows sorted by column 'col_name'.

        Args:
            col_name(str): name of column for sorting.
            reversed(bool): reversed or not

        Returns:
            Table: sorted table.
        """
        new_table = self.copy()
        new_table.rows.sort(key=itemgetter(col_name), reverse=reversed)
        return new_table

    def copy(self):
        """ Return copy of this Table. """
        rows = (
            map(itemgetter(1), row)
            for row in self.rows
        )
        return Table(rows, col_names=self.col_names)

    @property
    def cols_count(self):
        """ Count of column names """
        return len(self.col_names)

    @property
    def rows_count(self):
        """ Count of rows """
        return len(self.rows)

    @property
    def headers(self):
        """ List of column names """
        return self.col_names[:]
