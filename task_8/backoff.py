def backoff(max_tries, retry_on):
    # check what retry_on it is excepts
    for exp in retry_on:
        if isinstance(exp, Exception):
            raise ValueError(f'{exp} is not Exception')

    def _deco(func):
        def _wrap(*args, **kwargs):
            for i in range(max_tries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except retry_on:
                    print(f'Failed {i} time(s)')
            return _wrap

    return _deco
