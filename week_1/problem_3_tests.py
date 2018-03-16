from unittest import TestCase

from .problem_3 import Matrix, DimensionError


class TestMatrix(TestCase):

    def setUp(self):
        self.inputs = {
            'simple': ((1, 2, 3), (4, 5, 6)),
            'simple2': ((10, 20, 30), (40, 50, 60)),
            'fail': ((1, 2), (1,)),
            '3x4': ((1, 2, 3,), (4, 5, 6), (7, 8, 9), (10, 11, 12)),
            'col': ((3,), (2,), (1,)),
        }

    def matrix(self, key):
        return Matrix(*self.inputs[key])

    def test_init(self):
        m = self.matrix('simple')
        self.assertEqual(
            repr(m),
            "1.0 2.0 3.0 \n"
            "4.0 5.0 6.0 "
        )

    def test_init_fail(self):
        with self.assertRaises(Exception):
            self.matrix('fail')

    def test_slice(self):
        m = self.matrix('simple')
        self.assertEqual(
            repr(m[0]),
            "1.0 2.0 3.0 "
        )
        self.assertEqual(
            repr(m[1]),
            "4.0 5.0 6.0 "
        )
        self.assertEqual(
            repr(m[-1]),
            "4.0 5.0 6.0 "
        )
        self.assertEqual(
            repr(m[::-1]),
            "4.0 5.0 6.0 \n"
            "1.0 2.0 3.0 "
        )

    def test_slice_binary(self):
        m = self.matrix('3x4')
        self.assertEqual(
            repr(m[0:2]),
            "1.0 2.0 3.0 \n"
            "4.0 5.0 6.0 "
        )
        self.assertEqual(
            m[1, 1],
            5.0
        )
        self.assertEqual(
            repr(m[0:2, 0:2]),
            "1.0 2.0 \n"
            "4.0 5.0 "
        )
        self.assertEqual(
            repr(m[0:2, 0:2]),
            "1.0 2.0 \n"
            "4.0 5.0 "
        )
        self.assertEqual(
            repr(m[::-1, ::-1]),
            "12.0 11.0 10.0 \n"
            "9.0  8.0  7.0  \n"
            "6.0  5.0  4.0  \n"
            "3.0  2.0  1.0  "
        )

    def test_none(self):
        m = Matrix()
        self.assertEqual(
            repr(m),
            '',
        )
        m = self.matrix('simple')
        self.assertEqual(
            m[1:1],
            None,
        )

    def test_set_one_item(self):
        m = self.matrix('simple')
        m[1, 1] = 0
        self.assertEqual(m[1, 1], 0)
        self.assertEqual(m[1, 0], 4)

    def test_add(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('simple2')
        m3 = m1 + m2
        self.assertEqual(
            repr(m3),
            "11.0 22.0 33.0 \n"
            "44.0 55.0 66.0 "
        )
        self.assertNotEqual(id(m1), id(m3))

        old_id = id(m1)
        m1 += m2
        new_id = id(m1)
        self.assertEqual(old_id, new_id)

    def test_add_raise(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('3x4')
        with self.assertRaises(DimensionError):
            m1 + m2

    def test_sign(self):
        m = self.matrix('simple')

        self.assertEqual(
            repr(-m),
            "-1.0 -2.0 -3.0 \n"
            "-4.0 -5.0 -6.0 "
        )

        self.assertEqual(repr(-(-m)), repr(m))

    def test_sub(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('simple2')
        m3 = m2 - m1
        self.assertEqual(
            repr(m3),
            "9.0  18.0 27.0 \n"
            "36.0 45.0 54.0 "
        )
        self.assertNotEqual(id(m1), id(m3))

        old_id = id(m1)
        m1 -= m2
        new_id = id(m1)
        self.assertEqual(old_id, new_id)

    def test_eq(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('simple')
        m3 = self.matrix('simple2')

        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)

    def test_mul(self):
        m1 = self.matrix('simple')
        old_id = id(m1)

        val = 1.5
        m1 *= val
        new_id = id(m1)
        self.assertEqual(
            repr(m1),
            "1.5 3.0 4.5 \n"
            "6.0 7.5 9.0 "
        )
        self.assertEqual(old_id, new_id)

        m2 = m1 * 2
        self.assertEqual(
            repr(m2),
            "3.0  6.0  9.0  \n"
            "12.0 15.0 18.0 "
        )
        self.assertNotEqual(old_id, id(m2))

        m3 = 2 * m1
        self.assertEqual(m2, m3)

    def test_pow(self):
        m1 = self.matrix('simple')
        old_id = id(m1)

        val = 2
        m1 **= val
        new_id = id(m1)
        self.assertEqual(
            repr(m1),
            "1.0  4.0  9.0  \n"
            "16.0 25.0 36.0 "
        )
        self.assertEqual(old_id, new_id)

        m1 = self.matrix('simple')
        m2 = m1 ** 2
        self.assertEqual(
            repr(m2),
            "1.0  4.0  9.0  \n"
            "16.0 25.0 36.0 "
        )
        self.assertNotEqual(id(m1), id(m2))

    def test_transpose(self):
        m1 = self.matrix('simple')
        m2 = m1.T
        m3 = m2.T

        self.assertNotEqual(m1, m2)
        self.assertEqual(m1, m3)

    def test_matmul(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('col')
        m3 = m1 @ m2
        self.assertEqual(
            repr(m3),
            "10.0 \n"
            "28.0 "
        )

        m2 = m1.T
        m3 = m1 @ m2
        self.assertEqual(
            repr(m3),
            "14.0 32.0 \n"
            "32.0 77.0 "
        )
