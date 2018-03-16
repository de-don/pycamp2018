from unittest import TestCase

from .problem_3 import Matrix, DimensionError


class TestMatrix(TestCase):

    def setUp(self):
        self.inputs = {
            'simple': ((1, 2, 3), (4, 5, 6)),
            'simple2': ((10, 20, 30), (40, 50, 60)),
            'fail': ((1, 2), (1,)),
            '3x4': ((1, 2, 3,), (4, 5, 6), (7, 8, 9), (10, 11, 12)),
        }

    def test_init(self):
        m = Matrix(*self.inputs['simple'])
        self.assertEqual(
            repr(m),
            "1.0 2.0 3.0 \n"
            "4.0 5.0 6.0 "
        )

    def test_init_fail(self):
        with self.assertRaises(Exception):
            Matrix(*self.inputs['fail'])

    def test_slice(self):
        m = Matrix(*self.inputs['simple'])
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
        m = Matrix(*self.inputs['3x4'])
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
        m = Matrix(*self.inputs['simple'])
        self.assertEqual(
            m[1:1],
            None,
        )

    def test_set_one_item(self):
        m = Matrix(*self.inputs['simple'])
        m[1, 1] = 0
        self.assertEqual(m[1, 1], 0)
        self.assertEqual(m[1, 0], 4)

    def test_add(self):
        m1 = Matrix(*self.inputs['simple'])
        m2 = Matrix(*self.inputs['simple2'])
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
        m1 = Matrix(*self.inputs['simple'])
        m2 = Matrix(*self.inputs['3x4'])
        with self.assertRaises(DimensionError):
            m1 + m2
