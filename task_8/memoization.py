from functools import wraps


def memoization(func):
    """ Decorator to cache function results for same arguments. """
    cache = {}

    @wraps(func)
    def _wrap(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        result = cache.get(key, None)
        if result:
            print("It's cached")
            return result

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return _wrap
