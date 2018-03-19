import operator
from functools import wraps, reduce
from itertools import chain, filterfalse


def self_and_other_has_equal_type(func):
    @wraps(func)
    def wrapper(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"{self.__class__} != {other.__class__}")
        return func(self, other)

    return wrapper


class Set:
    """ Create collection which consist unique elements."""
    _items = None

    def __init__(self, iterable=None):
        items = list()

        if iterable:
            for item in iterable:
                if item not in items:
                    items.append(item)

        self._items = items

    def __repr__(self):
        if self._items:
            return '{%s}' % ', '.join(map(str, self._items))
        else:
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
    @self_and_other_has_equal_type
    def __lt__(self, other):
        """ all items from self contains in other, but other != self """
        return len(self) < len(other) and all(map(other.__contains__, self))

    @self_and_other_has_equal_type
    def __le__(self, other):
        """ all items from self contains in other"""
        return len(self) <= len(other) and all(map(other.__contains__, self))

    @self_and_other_has_equal_type
    def __ge__(self, other):
        return other <= self

    @self_and_other_has_equal_type
    def __gt__(self, other):
        return other < self

    @self_and_other_has_equal_type
    def issubset(self, other):
        """ Equal self <= other """
        return self <= other

    @self_and_other_has_equal_type
    def issuperset(self, other):
        """ Equal self >= other """
        return self >= other

    @self_and_other_has_equal_type
    def isdisjoint(self, other):
        """ Return True if two Sets have a null intersection."""
        return not any(map(self.__contains__, other))

    @self_and_other_has_equal_type
    def __eq__(self, other):
        return len(self) == len(other) and all(map(self.__contains__, other))

    ##################################################
    # union
    ##################################################

    @self_and_other_has_equal_type
    def __or__(self, other):
        return Set(chain(self, other))

    def union(self, *args):
        """ Return the union of Sets as a new Set. """
        return reduce(operator.or_, args, self)

    @self_and_other_has_equal_type
    def __ior__(self, other):
        tmp_set = self | other
        self._items = tmp_set._items
        return self

    def update(self, *args):
        """ Update a Set with the union of itself and others. """
        tmp_set = self.union(*args)
        self._items = tmp_set._items
        return self

    ##################################################
    # intersection
    ##################################################

    @self_and_other_has_equal_type
    def __and__(self, other):
        return Set(filter(other.__contains__, self))

    def intersection(self, *args):
        """ Return the intersection of two Sets as a new Set. """
        return reduce(operator.and_, args, self)

    @self_and_other_has_equal_type
    def __iand__(self, other):
        tmp_set = self & other
        self._items = tmp_set._items
        return self

    def intersection_update(self, *args):
        """ Update a Set with the intersection of itself and another."""
        tmp_set = self.intersection(*args)
        self._items = tmp_set._items
        return self

    ##################################################
    # difference
    ##################################################

    @self_and_other_has_equal_type
    def __sub__(self, other):
        return Set(filterfalse(other.__contains__, self))

    def difference(self, *args):
        """ Return the difference of two or more Sets as a new Set. """
        return reduce(operator.sub, args, self)

    @self_and_other_has_equal_type
    def __isub__(self, other):
        tmp_set = self - other
        self._items = tmp_set._items
        return self

    def difference_update(self, *args):
        """ Remove all elements of another Set from this Set. """
        tmp_set = self.difference(*args)
        self._items = tmp_set._items
        return self

    ##################################################
    # symmetric_difference
    ##################################################

    @self_and_other_has_equal_type
    def __xor__(self, other):
        return (self | other) - (self & other)

    def symmetric_difference(self, *args):
        """ Return the symmetric difference of two Sets as a new Set."""
        return reduce(operator.xor, args, self)

    @self_and_other_has_equal_type
    def __ixor__(self, other):
        tmp_set = self ^ other
        self._items = tmp_set._items
        return self

    def symmetric_difference_update(self, *args):
        """ Update a Set with the symmetric diff. of itself and another."""
        tmp_set = self.symmetric_difference(*args)
        self._items = tmp_set._items
        return self

    ##################################################
    # other methods
    ##################################################

    def copy(self):
        """ Return a copy of a Set. """
        return Set(self)

    def add(self, item):
        """ Add an item to a Set

        This is not change Set, if it's already contain an item.
        """
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
