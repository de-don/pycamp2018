from functools import wraps
from datetime import datetime


def dummy_logger(func):
    fmt = 'Called {name}(args={args}, kwargs={kwargs}) called at {time}'

    @wraps(func)
    def _wrap(*args, **kwargs):
        time = datetime.now().strftime("")
        name = func.__name__
        print(fmt.format(name=name, args=args, kwargs=kwargs, time=time))
        return func(*args, **kwargs)

    return _wrap


@dummy_logger
def sqrt(x):
    return x**.5


print(sqrt(x=10))
