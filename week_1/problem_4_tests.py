from unittest import TestCase

from .problem_4 import Set


class TestSet(TestCase):

    def test_init(self):
        l = [1, 2, 3]
        s = Set(l)
        self.assertSetEqual(s, set(l))

        l = [1, 2, 3, 4, 4, 3]
        s = Set(l)
        self.assertSetEqual(s, set(l))

        l = [1, 1, 1]
        s = Set(l)
        self.assertSetEqual(s, set(l))

        l = []
        s = Set(l)
        self.assertSetEqual(s, set(l))

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

    def test_operations_union(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 4, 5))
        s3 = Set([7, 9])

        s4 = Set((1, 2, 3, 4, 5))
        s5 = Set((1, 2, 3, 4, 5, 7, 9))

        self.assertSetEqual(s1.union(s2), s4)
        self.assertSetEqual(s1.union(s2, s3), s5)
        s1.update(s2, s3)
        self.assertSetEqual(s1, s5)
        s2 |= s3
        self.assertNotEqual(s2, Set((3, 4, 5)))

    def test_operations_isdisjoint(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 4, 5))
        s3 = Set([7, 9])

        self.assertTrue(s1.isdisjoint(s3))
        self.assertFalse(s1.isdisjoint(s2))

    def test_operations_intersection(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 2, 5))
        s3 = Set([7, 9])

        self.assertSetEqual(s1.intersection(s2), Set((2, 3)))
        self.assertSetEqual(s1.intersection(s2, s3), Set())
        s1.intersection_update(s2)
        self.assertSetEqual(s1, Set((2, 3)))
        s2 &= Set([2, 3])
        self.assertSetEqual(s1, Set([2, 3]))

    def test_operations_difference(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 5))
        s3 = Set([1])

        self.assertSetEqual(s1.difference(s2), Set((1, 2)))
        self.assertSetEqual(s1.difference(s2, s3), Set((2,)))

        s1.difference_update(s2, s3)
        self.assertSetEqual(s1, Set((2,)))
        s2 -= Set([5, 1])
        self.assertSetEqual(s2, Set([3]))

    def test_operations_symmetric_difference(self):
        s1 = Set((1, 2, 3))
        s2 = Set((3, 5))
        self.assertSetEqual(s1 ^ s2, Set((1, 2, 5)))

        s1 = Set((1, 2))
        s2 = Set((1, 2))
        self.assertSetEqual(s1 ^ s2, Set())

        s1 = Set((1, 2, 3, 4, 5))
        s2 = Set((2, 5, 9, 11))
        s3 = Set((6, 7, 8, 9))
        s4 = s1.symmetric_difference(s2, s3)

        self.assertSetEqual(s4, Set([1, 3, 4, 6, 7, 8, 11]))

        s1.symmetric_difference_update(s2, s3)
        self.assertSetEqual(s1, Set([1, 3, 4, 6, 7, 8, 11]))
        s2 ^= s3
        self.assertSetEqual(s2, Set([2, 5, 11, 6, 7, 8]))

    def test_copy(self):
        s1 = Set([1, 5, -1, 2, 3, 5, -5])
        s2 = s1.copy()
        self.assertSetEqual(s1, s2)
        self.assertNotEqual(id(s1), id(s2))

    def test_other_methods(self):
        s1 = Set([1, 2, 3, 4, 5])
        s2 = s1.copy()

        s2.add(5)
        self.assertSetEqual(s2, s1)
        s2.add(6)
        self.assertSetEqual(s2, s1 | Set([6]))

        s2.remove(6)
        self.assertSetEqual(s1, s2)
        with self.assertRaises(KeyError):
            s2.remove(6)

        s2.discard(6)
        s2.discard(5)
        s2 = s1.copy()

        l = len(s2)
        q = s2.pop()
        self.assertTrue(q in s1)
        self.assertTrue(len(s2) == l - 1)
        self.assertTrue(s2 < s1)
        self.assertFalse(s2 > s1)

        s2.clear()

        with self.assertRaises(KeyError):
            s2.pop()
