from itertools import product, compress
from unittest import TestCase

from problem_5.factory import dict_factory, ProtectedError

# dictionaries for tests
dict_not_embedded = {'name': 'Denis', 'age': 22, 'lists': [1, 2, 3]}
dict_embedded = {
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
    permissions = dict(change=False, add=False, delete=False, protect=False)

    def setUp(self):
        self.cls = dict_factory("EditableRemovable", **self.permissions)

    def test_init_and_read_1(self):
        d = self.cls(dict_not_embedded)
        self.assertEqual(d.name, dict_not_embedded['name'])
        self.assertEqual(d.lists, dict_not_embedded['lists'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

    def test_init_and_read_2(self):
        d = self.cls(dict_embedded)
        self.assertEqual(d.skills.python, dict_embedded['skills']['python'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.skills.cpp

    def test_change_allow_1(self):
        if not self.permissions.get('change', False):
            return
        d1 = self.cls(dict_not_embedded)
        d1.name = 'Joan'
        self.assertEqual(d1.name, 'Joan')

    def test_change_denied_2(self):
        if self.permissions.get('change', False):
            return
        d2 = self.cls(dict_embedded)
        with self.assertRaises(PermissionError):
            d2.skills.python = 'guru'

    def test_add_allow_1(self):
        if not self.permissions.get('add', False):
            return
        d1 = self.cls(dict_not_embedded)
        d1.title = 'example'
        self.assertEqual(d1.title, 'example')

    def test_add_allow_2(self):
        if not self.permissions.get('add', False):
            return
        d2 = self.cls(dict_embedded)
        d2.skills.cpp = 'guru'
        self.assertEqual(d2.skills.cpp, 'guru')

    def test_add_denied_1(self):
        if self.permissions.get('add', False):
            return
        d1 = self.cls(dict_not_embedded)
        with self.assertRaises(PermissionError):
            d1.title = 'example'

    def test_add_denied_2(self):
        if self.permissions.get('add', False):
            return
        d2 = self.cls(dict_embedded)
        with self.assertRaises(PermissionError):
            d2.skills.cpp = 'guru'

    def test_delete_allow(self):
        if not self.permissions.get('delete', False):
            return
        d1 = self.cls(dict_not_embedded)
        del d1.name
        with self.assertRaises(KeyError):
            d1.name

    def test_delete_allow_2(self):
        if not self.permissions.get('delete', False):
            return
        d2 = self.cls(dict_embedded)
        del d2.skills.python
        with self.assertRaises(KeyError):
            d2.skills.python

    def test_delete_denied_1(self):
        if self.permissions.get('delete', False):
            return
        d1 = self.cls(dict_not_embedded)
        with self.assertRaises(PermissionError):
            del d1.name

    def test_delete_denied_2(self):
        if self.permissions.get('delete', False):
            return
        d2 = self.cls(dict_embedded)
        with self.assertRaises(PermissionError):
            del d2.skills.python

    def test_delete_protected_1(self):
        if not self.permissions.get('delete', False):
            return
        if not self.permissions.get('protect', False):
            return

        d1 = self.cls(dict_not_embedded, protected=['age'])
        with self.assertRaises(ProtectedError):
            del d1.age

    def test_delete_protected_2(self):
        if not self.permissions.get('delete', False):
            return
        if not self.permissions.get('protect', False):
            return
        d2 = self.cls(dict_embedded, protected=['age', 'skills.fortran'])
        with self.assertRaises(ProtectedError):
            del d2.skills.fortran
        with self.assertRaises(ProtectedError):
            del d2.skills

    def test_change_protected_1(self):
        if not self.permissions.get('change', False):
            return
        if not self.permissions.get('protect', False):
            return

        d1 = self.cls(dict_not_embedded, protected=['age'])
        with self.assertRaises(ProtectedError):
            d1.age = 23

    def test_change_protected_2(self):
        if not self.permissions.get('change', False):
            return
        if not self.permissions.get('protect', False):
            return

        d2 = self.cls(dict_embedded, protected=['age', 'skills.fortran'])

        with self.assertRaises(ProtectedError):
            d2.skills.fortran = 'junior'
        with self.assertRaises(ProtectedError):
            d2.skills = 'None'


# Test-factory for test all combinations of permissions
for change, add, delete, protect in product([False, True], repeat=4):
    name = ["Edit", "Add", "Del", "Protect"]
    flags = [change, add, delete, protect]
    class_name = "TestPermissions_" + "".join(compress(name, flags))

    # save variable in globals, in order to Unittests runner can see this
    attrs = {"permissions": dict(change=change, add=add, delete=delete,
                                 protect=protect)}
    globals()[class_name] = type(class_name, (FactoryReadableTest,), attrs)
