import operator
from functools import wraps, reduce
from itertools import chain, filterfalse


def params_some_type(func):
    @wraps(func)
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"{self.__class__.__name__} != {other.__class__.__name__}"
            )
        return func(self, other)

    return wrapper


class Set:
    """ Create collection which consist unique elements."""
    __slots__ = ('_items',)

    def __init__(self, iterable=None):
        self._items = list()
        if not iterable:
            return

        for item in iterable:
            self.add(item)

    def __repr__(self):
        if len(self):
            return '{%s}' % ', '.join(map(str, self))
        return 'set()'

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    ##################################################
    # comparison
    ##################################################
    @params_some_type
    def __lt__(self, other):
        """ all items from self contains in other, but other != self """
        return len(self) < len(other) and all(map(other.__contains__, self))

    @params_some_type
    def __le__(self, other):
        """ all items from self contains in other"""
        return len(self) <= len(other) and all(map(other.__contains__, self))

    @params_some_type
    def issubset(self, other):
        """ Equal self <= other """
        return self <= other

    @params_some_type
    def issuperset(self, other):
        """ Equal self >= other """
        return self >= other

    @params_some_type
    def isdisjoint(self, other):
        """ Return True if two Sets have a null intersection."""
        return not any(map(self.__contains__, other))

    @params_some_type
    def __eq__(self, other):
        return len(self) == len(other) and all(map(self.__contains__, other))

    ##################################################
    # union
    ##################################################

    @params_some_type
    def __or__(self, other):
        return Set(chain(self, other))

    __ror__ = __or__

    def union(self, *args):
        """ Return the union of Sets as a new Set. """
        return reduce(operator.or_, args, self)

    @params_some_type
    def __ior__(self, other):
        tmp_set = self | other
        self.copy_items(tmp_set)
        return self

    def update(self, *args):
        """ Update a Set with the union of itself and others. """
        tmp_set = self.union(*args)
        self.copy_items(tmp_set)
        return self

    ##################################################
    # intersection
    ##################################################

    @params_some_type
    def __and__(self, other):
        return Set(filter(other.__contains__, self))

    __rand__ = __and__

    def intersection(self, *args):
        """ Return the intersection of two Sets as a new Set. """
        return reduce(operator.and_, args, self)

    @params_some_type
    def __iand__(self, other):
        tmp_set = self & other
        self.copy_items(tmp_set)
        return self

    def intersection_update(self, *args):
        """ Update a Set with the intersection of itself and another."""
        tmp_set = self.intersection(*args)
        self.copy_items(tmp_set)
        return self

    ##################################################
    # difference
    ##################################################

    @params_some_type
    def __sub__(self, other):
        return Set(filterfalse(other.__contains__, self))

    def difference(self, *args):
        """ Return the difference of two or more Sets as a new Set. """
        return reduce(operator.sub, args, self)

    @params_some_type
    def __isub__(self, other):
        tmp_set = self - other
        self.copy_items(tmp_set)
        return self

    def difference_update(self, *args):
        """ Remove all elements of another Set from this Set. """
        tmp_set = self.difference(*args)
        self.copy_items(tmp_set)
        return self

    ##################################################
    # symmetric_difference
    ##################################################

    @params_some_type
    def __xor__(self, other):
        return (self | other) - (self & other)

    __rxor__ = __xor__

    def symmetric_difference(self, *args):
        """ Return the symmetric difference of two Sets as a new Set."""
        return reduce(operator.xor, args, self)

    @params_some_type
    def __ixor__(self, other):
        tmp_set = self ^ other
        self.copy_items(tmp_set)
        return self

    def symmetric_difference_update(self, *args):
        """ Update a Set with the symmetric diff. of itself and another."""
        tmp_set = self.symmetric_difference(*args)
        self.copy_items(tmp_set)
        return self

    ##################################################
    # other methods
    ##################################################

    @params_some_type
    def copy_items(self, other):
        """ method to copy items from other to self """
        self.clear()
        for i in other:
            self.add(i)

    def copy(self):
        """ Return a copy of a Set. """
        return Set(self)

    def add(self, item):
        """ Add an item to a Set

        This is not change Set, if it's already contain an item.
        """

        # check immutable
        from collections.abc import Hashable
        if not isinstance(item, Hashable):
            raise TypeError(f'unhashable type: \'{item.__class__.__name__}\'')

        if item not in self:
            self._items.append(item)

    def remove(self, item):
        """ Remove item from Set.

        Raises KeyError if an item not contains in Set.
        """
        if item not in self._items:
            raise KeyError(item)

        self._items.remove(item)

    def discard(self, item):
        """ Remove an item from a Set if it is a member, else nothing."""
        try:
            self.remove(item)
        except KeyError:
            pass

    def pop(self):
        """ Remove and return an element from Set.

        Raises KeyError if the Set is empty.
        """
        try:
            item = self._items.pop()
        except IndexError:
            raise KeyError('pop from an empty Set')
        return item

    def clear(self):
        """ Remove all elements from this Set. """
        self._items.clear()
