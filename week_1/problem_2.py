def merge_dicts(d1, d2):
    """ Merge dicts d1 and d2. If key exists in d1 and d2,
    a value will be an equal sum of values this key.

    Example:
        >> d1 = {"a": 1, "b":2}
        >> d2 = {"b": 3, "c":4}
        >> d3 = merge_dicts(d1, d2)
        >> d3
        {'a': 1, 'b': 5, 'c': 4}
    """

    d3 = d1.copy()
    for key, value in d2.items():
        if d3.get(key, None):
            d3[key] += value
        else:
            d3.update({key: value})

    return d3
