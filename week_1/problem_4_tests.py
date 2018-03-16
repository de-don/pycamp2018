from unittest import TestCase

from .problem_4 import Set


class TestSet(TestCase):

    def assertIterEqual(self, iterable1, iterable2, msg=None):
        l1 = list(iterable1)
        l2 = list(iterable2)

        self.assertListEqual(l1, l2, msg)

    def test_init(self):
        l = [1, 2, 3]
        s = Set(l)
        self.assertIterEqual(s, l)

        l = [1, 2, 3, 4, 4, 3]
        s = Set(l)
        self.assertIterEqual(s, set(l))

        l = [1, 1, 1]
        s = Set(l)
        self.assertIterEqual(s, set(l))

        l = []
        s = Set(l)
        self.assertIterEqual(s, set(l))

    def test_output(self):
        self.assertEqual(repr(Set([])), 'set()')
        self.assertEqual(repr(Set([1, 2, 3])), '{1, 2, 3}')
