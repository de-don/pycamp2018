from unittest import TestCase

from .calc import calc


class CalcTester(TestCase):
    def test_1(self):
        q = "100+200"
        r = 300.0
        self.assertEqual(calc(q), r)

    def test_2(self):
        q = "100+200-150"
        r = 150.0
        self.assertEqual(calc(q), r)

    def test_3(self):
        q = "20*11-200/10"
        r = 200.0
        self.assertEqual(calc(q), r)

    def test_4(self):
        q = "10*(1+2)"
        r = 30.0
        self.assertEqual(calc(q), r)
