from functools import wraps
from datetime import datetime

FORMAT_LOGGER = 'Called {name}(args={args}, kwargs={kwargs}) at {time}'


def dummy_logger(func):
    fmt = FORMAT_LOGGER

    @wraps(func)
    def _wrap(*args, **kwargs):
        time = datetime.now().strftime('%H:%M')
        name = func.__name__
        print(fmt.format(name=name, args=args, kwargs=kwargs, time=time))
        return func(*args, **kwargs)

    return _wrap
