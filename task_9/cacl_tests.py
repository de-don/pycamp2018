from unittest import TestCase

from .calc import calculate


class CalcTrueTester(TestCase):
    def test_1(self):
        q = "100 + 200"
        r = 300.0
        self.assertEqual(calculate(q), r)

    def test_2(self):
        q = "100+200 - 150"
        r = 150.0
        self.assertEqual(calculate(q), r)

    def test_3(self):
        q = "20*11-200/10"
        r = 200.0
        self.assertEqual(calculate(q), r)

    def test_4(self):
        q = "10 * (1+2)"
        r = 30.0
        self.assertEqual(calculate(q), r)

    def test_5(self):
        q = "2+2*2"
        r = 6.0
        self.assertEqual(calculate(q), r)

    def test_6(self):
        q = "2*2+2"
        r = 6.0
        self.assertEqual(calculate(q), r)

    def test_7(self):
        q = "0*2+1"
        r = 1.0
        self.assertEqual(calculate(q), r)

    def test_8(self):
        q = "((50/50+10)-5*2)*100.5-5.5"
        r = 95.0
        self.assertEqual(calculate(q), r)

    def test_8(self):
        q = "(2+2)*(2+2)"
        r = 16.0
        self.assertEqual(calculate(q), r)

    def test_9(self):
        q = "((1+1)+2)*(2+2)"
        r = 16.0
        self.assertEqual(calculate(q), r)

    ##############################################################
    # pow tests
    ##############################################################

    def test_pow_1(self):
        q = "10^2"
        r = 100.0
        self.assertEqual(calculate(q), r)

    def test_pow_2(self):
        q = "9^0.5"
        r = 3.0
        self.assertEqual(calculate(q), r)

    def test_pow_3(self):
        q = "10*2^2"
        r = 40.0
        self.assertEqual(calculate(q), r)

    def test_pow_4(self):
        q = "2^2*3"
        r = 12.0
        self.assertEqual(calculate(q), r)

    def test_pow_5(self):
        q = "(2+2)^2.5"
        r = 32.0
        self.assertEqual(calculate(q), r)

    def test_pow_6(self):
        q = "(2+2)^2/2"
        r = 8.0
        self.assertEqual(calculate(q), r)

    def test_pow_7(self):
        q = "(2+2)^(2/2)"
        r = 4.0
        self.assertEqual(calculate(q), r)


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
