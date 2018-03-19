from unittest import TestCase

from week_1.problem_5.main import SimpleDict


class SimpleDictTest(TestCase):
    def test_init(self):
        d = SimpleDict({'name': 'Denis', 'age': 22})

        self.assertEqual(d.name, 'Denis')
        self.assertEqual(d.age, 22)

        with self.assertRaises(KeyError):
            d.title

        with self.assertRaises(PermissionError):
            d.name = 'Jenya'

    def test_2d_dict(self):
        d = SimpleDict({'name': 'Denis', 'age': 22, 'skills': {
            'python': 'middle',
            'fortran': 'lower',
        }})

        self.assertEqual(d.name, 'Denis')
        self.assertEqual(d.age, 22)
        self.assertEqual(d.skills.python, 'middle')

        with self.assertRaises(KeyError):
            d.qwe = 1