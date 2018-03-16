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

        with self.assertRaises(TypeError):
            Set(1)

    def test_output(self):
        self.assertEqual(repr(Set([])), 'set()')
        self.assertEqual(repr(Set([1, 2, 3])), '{1, 2, 3}')

    def test_comp(self):
        s1 = Set((1, 2, 3))
        s2 = Set((0, 2, 1, 3, 2))
        s3 = Set((0, 2, 1, 3, 2, 1, 2, 3))

        self.assertTrue(s1 <= s2)
        self.assertTrue(s2 >= s1)
        self.assertTrue(s1.issubset(s2))

        self.assertTrue(s2 == s3)

        self.assertFalse(s1 >= s2)
        self.assertFalse(s2 <= s1)
        self.assertFalse(s1.issuperset(s2))

    def test_operations(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 4, 5))
        s3 = Set([7, 9])

        self.assertIterEqual(s1 | s2, Set((1, 2, 3, 4, 5)))
        self.assertIterEqual(s1.union(s2), Set((1, 2, 3, 4, 5)))

        self.assertIterEqual(s1 | s2 | s3, Set((1, 2, 3, 4, 5, 7, 9)))
        self.assertIterEqual(s1.union(s2, s3), Set((1, 2, 3, 4, 5, 7, 9)))

        self.assertTrue(s1.isdisjoint(s3))
        self.assertFalse(s1.isdisjoint(s2))