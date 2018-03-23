from unittest import TestCase

from task_5.factory import dict_factory, ProtectedError

# dictionaries for tests
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
    cls = dict_factory("SimpleDict")

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
    cls = dict_factory("EditableDict", change=True)

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


class ExpandableDictTest(TestCase):
    cls = dict_factory("ExpandableDict", change=True, add=True)

    def test_init(self):
        d = self.cls({'name': 'Denis', 'age': 22})
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])

        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # add new attr
        d.title = 'example'
        self.assertEqual(d.title, 'example')

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

        # add new attr
        d.skills.cpp = 'guru'
        self.assertEqual(d.skills.cpp, 'guru')

        # edit already exist attr
        d.skills.python = 'guru'
        self.assertEqual(d.skills.python, 'guru')

        # try to del attr
        with self.assertRaises(PermissionError):
            del d.skills.python


class RemovableDictTest(TestCase):
    cls = dict_factory("RemovableDict", change=True, add=True,
                                     delete=True)

    def test_init(self):
        d = self.cls({'name': 'Denis', 'age': 22})
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])

        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # add new attr
        d.title = 'example'
        self.assertEqual(d.title, 'example')

        # edit to already exist attr
        d.name = 'Joan'
        self.assertEqual(d.name, 'Joan')

        # del attr
        del d.name
        with self.assertRaises(KeyError):
            d.name

    def test_2d_dict(self):
        d = self.cls(dict_2)

        self.assertEqual(d.name, dict_2['name'])
        self.assertEqual(d.age, dict_2['age'])
        self.assertEqual(d.skills.python, dict_2['skills']['python'])

        # try get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        # add new attr
        d.skills.cpp = 'guru'
        self.assertEqual(d.skills.cpp, 'guru')

        # edit already exist attr
        d.skills.python = 'guru'
        self.assertEqual(d.skills.python, 'guru')

        # del attr
        del d.skills.python
        with self.assertRaises(KeyError):
            d.skills.python

        # try to del again
        with self.assertRaises(KeyError):
            del d.skills.python


class ProtectedDictTest(TestCase):
    permissions = dict(change=True, add=True, delete=True, protect=True)

    def setUp(self):
        self.cls = dict_factory("Protected", **self.permissions)

    def test_init_and_read(self):
        d = self.cls(dict_1, protected=['age'])
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        d = self.cls(dict_2, protected=['age', 'skills.fortran'])
        self.assertEqual(d.skills.python, dict_2['skills']['python'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.skills.cpp

    def test_change(self):
        d1 = self.cls(dict_1, protected=['age'])
        d2 = self.cls(dict_2, protected=['age', 'skills.fortran'])

        # try to edit already exist attr
        d1.name = 'Joan'
        d2.skills.python = 'guru'
        self.assertEqual(d1.name, 'Joan')
        self.assertEqual(d2.skills.python, 'guru')

        with self.assertRaises(ProtectedError):
            d1.age = 23
        with self.assertRaises(ProtectedError):
            d2.skills.fortran = 'junior'
        with self.assertRaises(ProtectedError):
            d2.skills = 'junior'

    def test_add(self):
        d1 = self.cls(dict_1, protected=['age'])
        d2 = self.cls(dict_2, protected=['age', 'skills.fortran'])

        d1.title = 'example'
        d2.skills.cpp = 'guru'
        self.assertEqual(d1.title, 'example')
        self.assertEqual(d2.skills.cpp, 'guru')

    def test_delete(self):
        d1 = self.cls(dict_1, protected=['age'])
        d2 = self.cls(dict_2, protected=['age', 'skills.fortran'])

        del d1.name
        del d2.skills.python
        with self.assertRaises(KeyError):
            d1.name
        with self.assertRaises(KeyError):
            d2.skills.python

        with self.assertRaises(ProtectedError):
            del d1.age
        with self.assertRaises(ProtectedError):
            del d2.skills.fortran
        with self.assertRaises(ProtectedError):
            del d2.skills
