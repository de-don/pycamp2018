from itertools import chain


class Set:
    _items = None

    def __init__(self, iterable=None):
        items = list()

        if iterable:
            for i in iterable:
                if i not in items:
                    items.append(i)

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

    def isdisjoint(self, other):
        for item in other:
            if item in self:
                return False
        return True

    def __le__(self, other):
        """ self <= other """
        for item in self:
            if item not in other:
                return False
        return True

    def issubset(self, other):
        return self <= other

    def __ge__(self, other):
        """ self >= other """
        for item in other:
            if item not in self:
                return False
        return True

    def issuperset(self, other):
        return self >= other

    def __eq__(self, other):
        return self <= other <= self

    def __or__(self, other):
        return Set(chain(self, other))

    def union(self, *args):
        s = self
        for other in args:
            s = s | other
        return s

    def __and__(self, other):
        items = []
        for item in self:
            if item in other:
                items.append(item)

        return Set(items)

    def intersection(self, *args):
        s = self
        for other in args:
            s = s & other
        return s

    def __sub__(self, other):
        items = []
        for item in self:
            if item not in other:
                items.append(item)

        return Set(items)

    def difference(self, *args):
        s = self
        for other in args:
            s = s - other
        return s

    def __xor__(self, other):
        return (self | other) - (self & other)

    def symmetric_difference(self, *args):
        s = self
        for other in args:
            s = s ^ other
        return s

    def copy(self):
        return Set(self)
