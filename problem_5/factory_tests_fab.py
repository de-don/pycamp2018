from unittest import TestCase
from itertools import product, compress

from problem_5.factory import dict_factory, ProtectedError

# dictionaries for tests
dict_1 = {'name': 'Denis', 'age': 22, 'lists': [1, 2, 3]}
dict_2 = {
    'name': 'Denis',
    'age': 22,
    'skills': {
        'python': 'middle',
        'fortran': 'lower',
    },
    'lists': [1, 2, 3],
}


# One test-class for create child classes with different permissions
class FactoryReadableTest(TestCase):
    permissions = dict(change=False, add=False, delete=False, protected=False)

    def setUp(self):
        self.cls = dict_factory("EditableRemovable", **self.permissions)

    def test_init_and_read_1(self):
        d = self.cls(dict_1)
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])
        self.assertEqual(d.lists, dict_1['lists'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

    def test_init_and_read_2(self):
        d = self.cls(dict_2)
        self.assertEqual(d.skills.python, dict_2['skills']['python'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.skills.cpp

    def test_change_allow(self):
        if not self.permissions.get('change', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)
        d1.name = 'Joan'
        d2.skills.python = 'guru'
        self.assertEqual(d1.name, 'Joan')
        self.assertEqual(d2.skills.python, 'guru')


    def test_change_denied(self):
        if self.permissions.get('change', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)
        with self.assertRaises(PermissionError):
            d1.name = 'Joan'
        with self.assertRaises(PermissionError):
            d2.skills.python = 'guru'

    def test_add_allow(self):
        if not self.permissions.get('add', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)

        d1.title = 'example'
        d2.skills.cpp = 'guru'
        self.assertEqual(d1.title, 'example')
        self.assertEqual(d2.skills.cpp, 'guru')

    def test_add_denied(self):
        if self.permissions.get('add', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)
        with self.assertRaises(PermissionError):
            d1.title = 'example'
        with self.assertRaises(PermissionError):
            d2.skills.cpp = 'guru'

    def test_delete_allow(self):
        if not self.permissions.get('delete', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)

        del d1.name
        del d2.skills.python
        with self.assertRaises(KeyError):
            d1.name
        with self.assertRaises(KeyError):
            d2.skills.python

    def test_delete_denied(self):
        if self.permissions.get('delete', False):
            return
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)
        with self.assertRaises(PermissionError):
            del d1.name
        with self.assertRaises(PermissionError):
            del d2.skills.python

    def test_delete_protected(self):
        if not self.permissions.get('delete', False):
            return
        if not self.permissions.get('protected', False):
            return

        d1 = self.cls(dict_1, protected=['age'])
        d2 = self.cls(dict_2, protected=['age', 'skills.fortran'])

        with self.assertRaises(ProtectedError):
            del d1.age
        with self.assertRaises(ProtectedError):
            del d2.skills.fortran
        with self.assertRaises(ProtectedError):
            del d2.skills

    def test_change_protected(self):
        if not self.permissions.get('change', False):
            return
        if not self.permissions.get('protected', False):
            return

        d1 = self.cls(dict_1, protected=['age'])
        d2 = self.cls(dict_2, protected=['age', 'skills.fortran'])

        with self.assertRaises(ProtectedError):
            d1.age = 23
        with self.assertRaises(ProtectedError):
            d2.skills.fortran = 'junior'
        with self.assertRaises(ProtectedError):
            d2.skills = 'None'


# Test-factory for test all combinations of permissions
for change, add, delete, protected in product([False, True], repeat=4):
    name = ["Edit", "Add", "Del", "Protected"]
    flags = [change, add, delete, protected]
    class_name = "TestPermissions_" + "".join(compress(name, flags))

    # save variable in globals, in order to Unittests runner can see this
    attrs = {"permissions": dict(change=change, add=add, delete=delete,
                                 protected=protected)}
    globals()[class_name] = type(class_name, (FactoryReadableTest,), attrs)
