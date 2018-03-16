class Set:
    _items = None

    def __init__(self, iterable):
        items = list()

        for i in iterable:
            if i not in items:
                items.append(i)

        self._items = items
