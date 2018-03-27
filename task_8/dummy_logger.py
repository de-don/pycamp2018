from functools import wraps


def dummy_logger(func):
    @wraps(func)
    def _wrap(*args, **kwargs):
        time = "12:48"
        name = func.__name__
        text = f'`{name}` called at {time} with args={args} and kwargs={kwargs}'
        print(text)
        return func(*args, **kwargs)

    return _wrap

