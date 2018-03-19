from unittest import TestCase

from .problem_3 import DimensionError, Matrix


class TestMatrix(TestCase):

    def setUp(self):
        self.inputs = {
            'simple': ((1, 2, 3), (4, 5, 6)),
            'simple2': ((10, 20, 30), (40, 50, 60)),
            'fail': ((1, 2), (1,)),
            '3x4': ((1, 2, 3,), (4, 5, 6), (7, 8, 9), (10, 11, 12)),
            'col': ((3,), (2,), (1,)),
            '2x2': ((1, 2), (3, 4))
        }

    def matrix(self, key):
        return Matrix(self.inputs[key])

    def test_init(self):
        m = self.matrix('simple')
        self.assertListEqual(
            list(m),
            [[1.0, 2.0, 3.0],
             [4.0, 5.0, 6.0]],
        )

    def test_init_fail(self):
        with self.assertRaises(Exception):
            self.matrix('fail')

    def test_str(self):
        m = self.matrix('simple')
        self.assertEqual(
            str(m),
            "[Matrix 2x3]\n"
            " 1.0  2.0  3.0\n"
            " 4.0  5.0  6.0",
        )
        self.assertEqual(
            repr(m),
            " 1.0  2.0  3.0\n"
            " 4.0  5.0  6.0",
        )

    def test_slice(self):
        m = self.matrix('simple')
        self.assertListEqual(
            list(m[0]),
            [[1.0, 2.0, 3.0]],
        )
        self.assertListEqual(
            list(m[1,]),
            [[4.0, 5.0, 6.0]],
        )
        self.assertListEqual(
            list(m[-1]),
            [[4.0, 5.0, 6.0]],
        )
        self.assertListEqual(
            list(m[::-1]),
            [[4.0, 5.0, 6.0],
             [1.0, 2.0, 3.0]],
        )

    def test_slice_binary(self):
        m = self.matrix('3x4')
        self.assertListEqual(
            list(m[0:2]),
            [[1.0, 2.0, 3.0],
             [4.0, 5.0, 6.0]],
        )
        self.assertEqual(m[1, 1], 5.0)
        self.assertEqual(m[1:1, 0], None)
        self.assertListEqual(
            list(m[0:2, 0:2]),
            [[1.0, 2.0],
             [4.0, 5.0]],
        )
        self.assertListEqual(
            list(m[0:2, 0:2]),
            [[1.0, 2.0],
             [4.0, 5.0]],
        )
        self.assertListEqual(
            list(m[::-1, ::-1]),
            [[12.0, 11.0, 10.0],
             [9.0, 8.0, 7.0],
             [6.0, 5.0, 4.0],
             [3.0, 2.0, 1.0]],
        )

    def test_slice_raise(self):
        m1 = self.matrix('simple')
        with self.assertRaises(TypeError):
            m1[1, 1, 1]
        with self.assertRaises(TypeError):
            m1['ser']
        with self.assertRaises(TypeError):
            m1[.1]
        with self.assertRaises(TypeError):
            m1[.1:.1]
        with self.assertRaises(TypeError):
            m1[1, .1]

    def test_none(self):
        m = Matrix()
        self.assertEqual(list(m), [])
        m = self.matrix('simple')
        self.assertEqual(m[1:1], None)

    def test_set_one_item(self):
        m = self.matrix('simple')
        m[1, 1] = 0
        self.assertEqual(m[1, 1], 0)
        self.assertEqual(m[1, 0], 4)

        with self.assertRaises(TypeError):
            m[1, 1] = "test"
        with self.assertRaises(TypeError):
            m[0:1, 1] = 1

    def test_set_row(self):
        m = self.matrix('simple')

        m[1] = (-1, -2, -3)

        self.assertListEqual(
            list(m),
            [[1.0, 2.0, 3.0],
             [-1.0, -2.0, -3.0]],
        )

        with self.assertRaises(TypeError):
            m[1] = "test"

        with self.assertRaises(DimensionError):
            m[0] = (1, 2)

    def test_add(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('simple2')
        m3 = m1 + m2
        self.assertListEqual(
            list(m3),
            [[11.0, 22.0, 33.0],
             [44.0, 55.0, 66.0]],
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

        with self.assertRaises(TypeError):
            1 + m1

    def test_sign(self):
        m = self.matrix('simple')
        self.assertListEqual(
            list(-m),
            [[-1.0, -2.0, -3.0],
             [-4.0, -5.0, -6.0]],
        )
        self.assertEqual(-(-m), m)
        self.assertEqual(+m, m)

    def test_sub(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('simple2')
        m3 = m2 - m1
        self.assertListEqual(
            list(m3),
            [[9.0, 18.0, 27.0],
             [36.0, 45.0, 54.0]],
        )
        self.assertNotEqual(id(m1), id(m3))

        old_id = id(m1)
        m1 -= m2
        new_id = id(m1)
        self.assertEqual(old_id, new_id)

    def test_sub_raise(self):
        m1 = self.matrix('simple')
        m2 = self.matrix('3x4')
        with self.assertRaises(DimensionError):
            m1 - m2

        with self.assertRaises(TypeError):
            1 - m1

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
        self.assertListEqual(
            list(m1),
            [[1.5, 3.0, 4.5],
             [6.0, 7.5, 9.0]]
        )
        self.assertEqual(old_id, new_id)

        m2 = m1 * 2
        self.assertListEqual(
            list(m2),
            [[3.0, 6.0, 9.0],
             [12.0, 15.0, 18.0]],
        )
        self.assertNotEqual(old_id, id(m2))

        m3 = 2 * m1
        self.assertEqual(m2, m3)

    def test_mul_raise(self):
        m1 = self.matrix('simple')
        with self.assertRaises(TypeError):
            m1 * 'test'

    def test_pow(self):
        m1 = self.matrix('2x2')
        m2 = self.matrix('2x2')
        old_id = id(m2)

        val = 2
        m2 **= val
        new_id = id(m2)
        self.assertEqual(m2, m1 @ m1)
        self.assertEqual(old_id, new_id)

        m1 = self.matrix('2x2')
        m2 = m1 ** 2
        self.assertEqual(m1 ** 3, m1 @ m1 @ m1)
        self.assertNotEqual(id(m1), id(m2))

        m2 = m1 ** 0
        self.assertEqual(m2, Matrix.ones(2))

    def test_pow_raise(self):
        m1 = self.matrix('simple')
        with self.assertRaises(TypeError):
            m1 ** 'test'

        with self.assertRaises(DimensionError):
            m1 ** 2

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
        self.assertListEqual(
            list(m3),
            [[10.0],
             [28.0]],
        )
        m1 @= m2
        self.assertEqual(m1, m3)

        m1 = self.matrix('simple')
        m2 = m1.T
        m3 = m1 @ m2
        self.assertListEqual(
            list(m3),
            [[14.0, 32.0],
             [32.0, 77.0]],
        )

    def test_matmul_raise(self):
        m1 = self.matrix('simple')
        with self.assertRaises(TypeError):
            m1 @= "test"

        m2 = self.matrix('3x4')
        with self.assertRaises(DimensionError):
            m1 @ m2

    def test_zeros(self):
        m = Matrix.zeros(2, 3)
        self.assertListEqual(
            list(m),
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
        )

    def test_ones(self):
        m = Matrix.ones(3)
        self.assertListEqual(
            list(m),
            [[1.0, 0.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0]]
        )
