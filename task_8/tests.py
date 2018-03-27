import io

from .dummy_logger import dummy_logger, FORMAT_LOGGER
from unittest import TestCase
from contextlib import redirect_stdout
from datetime import datetime


class DummyLoggerTest(TestCase):
    def test_pow_func(self):
        @dummy_logger
        def pow(x, p=.5):
            return x ** p

        f = io.StringIO()
        with redirect_stdout(f):
            s = pow(9, p=.2)

        result = FORMAT_LOGGER.format(
            name='pow',
            args=(9,),
            kwargs={'p': .2},
            time=datetime.now().strftime('%H:%M'),  # may be not working
        ) + "\n"
        self.assertEqual(f.getvalue(), result)
