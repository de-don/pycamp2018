from functools import wraps


def backoff(max_tries, retry_on):
    """ Factory for creating a decorator that repeats a function call on errors

    Args:
        max_tries(int): max retries of call function.
        retry_on(tuple): tuple of Excepts
    """

    # check what retry_on it is excepts
    for exp in retry_on:
        if not issubclass(exp, BaseException):
            raise ValueError(f'{exp} is not Exception.')

    def _deco(func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            for i in range(max_tries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except retry_on:
                    print(f'Failed {i+1} time(s).')
            print(f'Retries is end.')
        return _wrap

    return _deco
