import io
from contextlib import redirect_stdout
from datetime import datetime
from unittest import TestCase

from .backoff import backoff
from .composer import composer
from .dummy_logger import FORMAT_LOGGER, dummy_logger
from .memoization import memoization


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


class BackoffTest(TestCase):
    def test_success(self):
        @backoff(max_tries=3, retry_on=(ValueError,))
        def to_int(iter_x):
            x = next(iter_x)
            return int(x)

        array = iter(['false', 'hello', '100'])

        f = io.StringIO()
        with redirect_stdout(f):
            number = to_int(array)
        output = f.getvalue()

        self.assertEqual(number, 100)
        self.assertEqual(output, 'Failed 1 time(s).\nFailed 2 time(s).\n')

    def test_none(self):
        @backoff(max_tries=2, retry_on=(TypeError, ValueError))
        def to_int(iter_x):
            x = next(iter_x)
            return int(x)

        array = iter(['false', 'hello', '100'])

        f = io.StringIO()
        with redirect_stdout(f):
            number = to_int(array)
        output = f.getvalue()

        self.assertEqual(number, None)
        self.assertEqual(
            output,
            'Failed 1 time(s).\n'
            'Failed 2 time(s).\n'
            'Retries is end.\n'
        )

    def test_raise(self):
        @backoff(max_tries=2, retry_on=(TypeError, StopIteration))
        def to_int(iter_x):
            x = next(iter_x)
            return int(x)

        array = iter(['false', 'hello', '100'])

        with self.assertRaises(ValueError):
            to_int(array)

    def test_raise_exp(self):
        with self.assertRaises(ValueError):
            @backoff(max_tries=2, retry_on=(str, int))
            def _(x):
                return x


class ComposerTest(TestCase):
    def test_example(self):
        def capitalize(string):
            return string.title()

        def newlines(string):
            return string.replace(' ', '\n')

        beautify = composer(capitalize, newlines)

        result = beautify('hello world')
        self.assertEqual(result, 'Hello\nWorld')

    def test_two_args(self):
        def swap(var1, var2):
            return var2, var1

        def muls(var1, var2):
            return var1 * 10, var2 * 20

        comlex = composer(swap, muls)

        result = comlex(10, 20)
        self.assertEqual(result, (200, 200))
        result = comlex(20, 10)
        self.assertEqual(result, (100, 400))

    def test_different(self):
        def split_slash(string):
            str1, str2 = string.split("/", 1)
            return str1, str2

        def join_backslash(var1, var2):
            return "\\".join((var1, var2,))

        replace_slash = composer(split_slash, join_backslash)

        result = replace_slash("home/page")
        self.assertEqual(result, "home\\page")

    def test_different_raise(self):
        def split_slash(string):
            str1, str2 = string.split("/")  ###
            return str1, str2

        def join_backslash(var1, var2):
            return "\\".join((var1, var2,))

        replace_slash = composer(split_slash, join_backslash)

        with self.assertRaises(ValueError):
            result = replace_slash("home/page/home")
