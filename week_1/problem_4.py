class Set:
    _items = None

    def __init__(self, iterable=None):
        items = list()

        try:
            for i in iterable:
                if i not in items:
                    items.append(i)
        except TypeError:
            pass

        self._items = items

    def __repr__(self):
        if self._items:
            return '{%s}' % ', '.join(map(str, self._items))
        else:
            return 'set()'

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, item):
        return self._items[item]
