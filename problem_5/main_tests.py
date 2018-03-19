from unittest import TestCase

from problem_5.main import SimpleDict, EditableDict

dict_1 = {'name': 'Denis', 'age': 22}
dict_2 = {
    'name': 'Denis',
    'age': 22,
    'skills': {
        'python': 'middle',
        'fortran': 'lower',
    }
}


class SimpleDictTest(TestCase):
    cls = SimpleDict

    def test_init(self):
        d = self.cls(dict_1)
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])

        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # try to add new attr
        with self.assertRaises(PermissionError):
            d.title = 'example'

        # try to edit already exist attr
        with self.assertRaises(PermissionError):
            d.name = 'Joan'

        # try to del attr
        with self.assertRaises(PermissionError):
            del d.name

    def test_2d_dict(self):
        d = self.cls(dict_2)

        self.assertEqual(d.name, dict_2['name'])
        self.assertEqual(d.age, dict_2['age'])
        self.assertEqual(d.skills.python, dict_2['skills']['python'])

        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # try to add new attr
        with self.assertRaises(PermissionError):
            d.skills.cpp = 'guru'

        # try to edit already exist attr
        with self.assertRaises(PermissionError):
            d.skills.python = 'guru'

        # try to del attr
        with self.assertRaises(PermissionError):
            del d.skills.python


class EditableDictTest(TestCase):
    cls = EditableDict

    def test_init(self):
        d = self.cls({'name': 'Denis', 'age': 22})
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])

        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # try to add new attr
        with self.assertRaises(PermissionError):
            d.title = 'example'

        # edit to already exist attr
        d.name = 'Joan'
        self.assertEqual(d.name, 'Joan')

        # try to del attr
        with self.assertRaises(PermissionError):
            del d.name

    def test_2d_dict(self):
        d = self.cls(dict_2)

        self.assertEqual(d.name, dict_2['name'])
        self.assertEqual(d.age, dict_2['age'])
        self.assertEqual(d.skills.python, dict_2['skills']['python'])

        # try get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # try add new attr
        with self.assertRaises(PermissionError):
            d.skills.cpp = 'guru'

        # edit already exist attr
        d.skills.python = 'guru'
        self.assertEqual(d.skills.python, 'guru')

        # try to del attr
        with self.assertRaises(PermissionError):
            del d.skills.python
