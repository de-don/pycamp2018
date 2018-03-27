def composer(*funcs):
    """ Function to compose many functions.

    Each subsequent function must take as many arguments as the previous
    one returns, else ValueError
    """
    def _wrap(*args):
        for func in funcs:
            if not isinstance(args, tuple):
                args = (args,)
            args = func(*args)
        return args

    return _wrap
