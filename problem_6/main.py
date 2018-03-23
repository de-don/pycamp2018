import datetime
import operator
from collections import OrderedDict
from contextlib import suppress
from functools import partial
from operator import itemgetter

from problem_6 import (
    CsvProvider,
    JsonProvider,
    Sqlite3Provider,
    HtmlProvider,
    YamlProvider
)

# supported types and their functions for filtering
SUPPORTED_FUNCS = {
    str: {
        'startswith': str.startswith,
        'endswith': str.endswith
    },
    int: {
        'gt': operator.gt,
        'lt': operator.lt,
        'ge': operator.ge,
        'le': operator.lt,
    },
    datetime.datetime: {
        'gt': operator.gt,
        'lt': operator.lt,
        'ge': operator.ge,
        'le': operator.le,
        'year': lambda x, value: x.year == value,
        'day': lambda x, value: x.day == value,
        'month': lambda x, value: x.month == value,
    },

}


class NotSupported(ValueError):
    """ Error raise which function not supported """
    pass


class Entry:
    """ Class for storing one table row. """

    def __init__(self, row, col_names):
        """
        Args:
            row(Iterable): iterator of items.
            col_names(Iterable): iterator of strings.
        """

        col_names = list(col_names)
        # check unique of column names
        if len(set(col_names)) < len(col_names):
            raise ValueError('Names of columns must be unique')

        # detection type of each element
        row = list(map(self.detect_type, list(row)))

        if len(row) != len(col_names):
            raise ValueError('Len(row) != Len(col_names)')

        self._items = OrderedDict(zip(col_names, row))

    @staticmethod
    def detect_type(item):
        """ Detect type of item: int, float, date or str """
        types = (
            int,
            float,
            lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'),
            lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d')
        )

        # check each type
        for cur_type in types:
            with suppress(ValueError, TypeError):
                new_item = cur_type(item)
                return new_item
        # if type not be found, leave str type
        return item

    def __getitem__(self, item):
        return self._items[item]

    def __str__(self):
        lines = (f'{title}: {value}' for title, value in self._items.items())
        return '\n'.join(lines)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Objects have different types')
        return self._items == other._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.items())

    def check(self, key, value, func=None):
        cell_value = self[key]

        if func is None:
            # if it is simple filtering without function
            return cell_value == value

        key_type = cell_value.__class__
        filter_function = SUPPORTED_FUNCS.get(key_type, {}).get(func, None)
        if filter_function is None:
            raise NotSupported(f'{func} not supported for {key_type.__name__}')

        return filter_function(cell_value, value)


class Table:
    """ Class for easy working with tables. """

    def __init__(self, rows, col_names):
        """
        Args:
            rows(Iterable): iterator of iterators. For example [[1, 2], [3, 4]].
            col_names(Iterable): iterator of strings.
        """
        self.col_names = list(col_names)

        self.rows = [Entry(row, self.col_names) for row in rows]

    def __str__(self):
        if not self.rows_count:
            return 'Empty'

        def gen_lines():
            """ Generator for create output lines.

            Yield strings in next format:
                '{row_num}:'
                '    {col_name_1}: {col_value_1}'
                '    {col_name_2}: {col_value_2}'
                ...
            """
            for row_num, row in enumerate(self.rows):
                yield f'{row_num}:'
                yield from ('    ' + line for line in str(row).splitlines())

        return '\n'.join(gen_lines())

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Not same types to compare')
        return self.rows == other.rows and self.col_names == self.col_names

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Index must be integer.')
        return self.rows[item]

    ##################################################
    # load methods
    ##################################################

    @classmethod
    def from_csv(cls, file_path, delimiter=';'):
        """ Load Table from csv file.

        Args:
            file_path(str): path to csv file.
            delimiter(str): csv delimiter.

        Returns:
            Table: Table created from data of the file.
        """
        return TableDataProvider(
            CsvProvider,
            file_path=file_path,
            delimiter=delimiter,
        ).load()

    @classmethod
    def from_json(cls, file_path):
        """ Load Table from json file.

        Args:
            file_path(str): path to json file.

        Returns:
            Table: Table created from data of the file.
        """
        return TableDataProvider(
            JsonProvider,
            file_path=file_path,
        ).load()

    @classmethod
    def from_sqlite3(cls, file_path, table_name):
        """ Load Table from sqlite3 database file.

        Args:
            file_path(str): path to sqlite3 file.
            table_name(str): table_name in database.

        Returns:
            Table: Table created from data of the database.
        """
        return TableDataProvider(
            Sqlite3Provider,
            file_path=file_path,
            table_name=table_name
        ).load()

    @classmethod
    def from_yaml(cls, file_path):
        """ Load Table from yaml file.

        Args:
            file_path(str): path to yaml file.

        Returns:
            Table: Table created from data of the file.
        """
        return TableDataProvider(
            YamlProvider,
            file_path=file_path,
        ).load()

    ##################################################
    # export methods
    ##################################################

    def to_csv(self, file_path, delimiter=';'):
        """ Save Table to csv file.

        Args:
            file_path(str): path to new csv file.
            delimiter(str): csv delimiter.
        """
        return TableDataProvider(
            CsvProvider,
            file_path=file_path,
            delimiter=delimiter,
        ).save(self)

    def to_json(self, file_path):
        """ Save Table to json file.

        Args:
            file_path(str): path to new json file.
        """
        return TableDataProvider(
            JsonProvider,
            file_path=file_path,
        ).save(self)

    def to_html(self, file_path):
        """ Save Table to html file.

        Args:
            file_path(str): path to new html file.
        """
        return TableDataProvider(
            HtmlProvider,
            file_path=file_path,
        ).save(self)

    def to_yaml(self, file_path):
        """ Save Table to yaml file.

        Args:
            file_path(str): path to new yaml file.
        """
        return TableDataProvider(
            YamlProvider,
            file_path=file_path,
        ).save(self)

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
        params = key.split('__', 1)
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
                Entry.check,
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

    def order_by(self, col_name, reverse=False):
        """ Return new Table which rows sorted by column 'col_name'.

        Args:
            col_name(str): name of column for sorting.
            reverse(bool): reversed or not

        Returns:
            Table: sorted table.
        """
        new_table = self.copy()
        new_table.rows.sort(key=itemgetter(col_name), reverse=reverse)
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

    def add_filter(types, name=None):
        """ Decorator fabric to create decorator for add filter function
        Args:
            types(tuple): tuple of supported types
            name: name filter, for using {column_name}__{name}=value

        Example:
            1) decorated and set custom name
            >> @Table.add_filter(types=(datetime.datetime, ), name="month")
            >> def date_month(x, value):
            >>     return x.month == value

            2) using built-in method and using his name ('lt')
            >> Table.add_filter(types=(int, datetime.datetime))(operator.lt)
        """

        def add_filter(func):
            """ Decorator which add func to SUPPORTED_FUNCS for filtering"""
            nonlocal name

            # check count arguments
            if hasattr(func, '__code__'):
                count_args = func.__code__.co_argcount
            else:
                count_args = 2
            if count_args != 2:
                raise TypeError("Decorated function must have 2 positional "
                                "arguments, but %s given" % count_args)

            # get new filter name
            name = func.__name__ if (name is None) else name

            # insert function to supported
            for current_type in types:
                if current_type not in SUPPORTED_FUNCS:
                    SUPPORTED_FUNCS[current_type] = {}
                SUPPORTED_FUNCS[current_type][name] = func

            return func

        return add_filter


class TableDataProvider:
    def __init__(self, proveder_class, **kwargs):
        self.provider = proveder_class(kwargs)

    def load(self):
        head, lines = self.provider.get_data()
        return Table(rows=lines, col_names=head)

    def save(self, table):
        head = table.headers
        lines = (map(str, map(itemgetter(1), row)) for row in table.rows)
        return self.provider.save_data(head, lines)
