def backoff(max_tries, retry_on):
    # check what retry_on it is excepts
    for exp in retry_on:
        if not issubclass(exp, BaseException):
            raise ValueError(f'{exp} is not Exception.')

    def _deco(func):
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
