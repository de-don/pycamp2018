from unittest import TestCase

from .calc import calculate


class CalcTrueTester(TestCase):
    def test_simple(self):
        data = (
            ("100 + 200", 300.0),
            ("100+200 - 150", 150.0),
            ("20*11-200/10", 200.0),
            ("10 * (1+2)", 30.0),
            ("2+2*2", 6.0),
            ("2*2+2", 6.0),
            ("0*2+1", 1.0),
            ("(2+2)*(2+2)", 16.0),
            ("((1+1)+2)*(2+2)", 16.0),
        )
        for i, (expr, result) in enumerate(data):
            with self.subTest(i=i):
                self.assertEqual(calculate(expr), result)

    ##############################################################
    # pow tests
    ##############################################################

    def test_pow(self):
        data = (
            ("10^2", 100.0),
            ("9^0.5", 3.0),
            ("10*2^2", 40.0),
            ("2^2*3", 12.0),
            ("(2+2)^2.5", 32.0),
            ("(2+2)^2/2", 8.0),
            ("(2+2)^(2/2)", 4),
        )
        for i, (expr, result) in enumerate(data):
            with self.subTest(i=i):
                self.assertEqual(calculate(expr), result)

    ##############################################################
    # negative
    ##############################################################

    def test_negative(self):
        data = (
            ("12-(-34)", 46.0),
            ("(-34)", -34.0),
            ("-0.5", -0.5),
            ("-0.5+5", 4.5),
            ("-0.5*-0.5", 0.25),
        )
        for i, (expr, result) in enumerate(data):
            with self.subTest(i=i):
                self.assertEqual(calculate(expr), result)

    ##############################################################
    # float without main number
    ##############################################################

    def test_float(self):
        data = (
            (".5+.5", 1.0),
            (".6*.6", 0.36),
        )
        for i, (expr, result) in enumerate(data):
            with self.subTest(i=i):
                self.assertEqual(calculate(expr), result)

    ##############################################################
    # difficult tests
    ##############################################################

    def test_difficult(self):
        data = (
            ("((2*5^2/50+10)-5*2)*100.5-5.5", 95.0),
            ("((50/50+10)-5*2)*100.5-5.5", 95.0),
        )
        for i, (expr, result) in enumerate(data):
            with self.subTest(i=i):
                self.assertEqual(calculate(expr), result)


class CalcErrorTester(TestCase):
    def test_1(self):
        q = "100/0"
        with self.assertRaises(ZeroDivisionError):
            calculate(q)

    def test_2(self):
        q = "100=100"
        with self.assertRaises(ValueError):
            calculate(q)

    def test_3(self):
        q = "10-(100+10"
        with self.assertRaises(ValueError):
            calculate(q)
