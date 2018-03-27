import io

from .dummy_logger import dummy_logger, FORMAT_LOGGER
from .memoization import memoization
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


class MemoizationTest(TestCase):
    def test_one_func(self):
        @memoization
        def wrong_pow(x, p=.2, a=5):
            return x ** p + a

        f = io.StringIO()
        with redirect_stdout(f):
            wrong_pow(1)
            wrong_pow(1)

        output = "It\'s cached\n"
        self.assertEqual(f.getvalue(), output)

    def test_one_func_some_values(self):
        @memoization
        def wrong_pow(x, p=.2, a=5):
            return x ** p + a

        f = io.StringIO()
        with redirect_stdout(f):
            wrong_pow(5, p=.3)
            wrong_pow(5, p=.4, a=10)
            wrong_pow(5, a=10, p=.4)

        output = "It\'s cached\n"
        self.assertEqual(f.getvalue(), output)

    def test_two_func(self):
        @memoization
        def wrong_pow(x, p=.2, a=5):
            return x ** p + a

        @memoization
        def true_pow(x, p=.2, a=5):
            return x ** p

        f = io.StringIO()
        with redirect_stdout(f):
            wrong_pow(5, p=.3)
            true_pow(5, p=.3)
            true_pow(5, p=.3)

        output = "It\'s cached\n"
        self.assertEqual(f.getvalue(), output)

