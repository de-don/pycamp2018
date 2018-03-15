from unittest import TestCase

from .problem_3 import Matrix


class TestMatrix(TestCase):

    def setUp(self):
        self.inputs = {
            'simple': ((1, 2, 3), (4, 5, 6)),
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
