from unittest import TestCase
from itertools import product, compress

from problem_5.factory import dict_factory
from problem_5.main_tests import (
    SimpleDictTest,
    EditableDictTest,
    ExpandableDictTest,
    RemovableDictTest,
)

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

# add tests from `main_tests` and change classes to results of factories
SimpleDictTest.cls = dict_factory("SimpleDict")
EditableDictTest.cls = dict_factory("EditableDict", change=True)
ExpandableDictTest.cls = dict_factory("ExpandableDict", change=True, add=True)
RemovableDictTest.cls = dict_factory("RemovableDict", change=True, add=True,
                                     delete=True)


# One test-class for create child classes with different permissions
class FactoryReadableTest(TestCase):
    permissions = dict(change=False, add=False, delete=False)

    def setUp(self):
        self.cls = dict_factory("EditableRemovable", **self.permissions)

    def test_init_and_read(self):
        d = self.cls(dict_1)
        self.assertEqual(d.name, dict_1['name'])
        self.assertEqual(d.age, dict_1['age'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.title

        d = self.cls(dict_2)
        self.assertEqual(d.skills.python, dict_2['skills']['python'])
        # try to get not exist attribute
        with self.assertRaises(KeyError):
            d.skills.cpp

    def test_change(self):
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)

        # try to edit already exist attr
        if self.permissions.get('change', False):
            d1.name = 'Joan'
            d2.skills.python = 'guru'
            self.assertEqual(d1.name, 'Joan')
            self.assertEqual(d2.skills.python, 'guru')
        else:
            with self.assertRaises(PermissionError):
                d1.name = 'Joan'
            with self.assertRaises(PermissionError):
                d2.skills.python = 'guru'

    def test_add(self):
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)

        if self.permissions.get('add', False):
            d1.title = 'example'
            d2.skills.cpp = 'guru'
            self.assertEqual(d1.title, 'example')
            self.assertEqual(d2.skills.cpp, 'guru')
        else:
            with self.assertRaises(PermissionError):
                d1.title = 'example'
            with self.assertRaises(PermissionError):
                d2.skills.cpp = 'guru'

    def test_delete(self):
        d1 = self.cls(dict_1)
        d2 = self.cls(dict_2)

        if self.permissions.get('delete', False):
            del d1.name
            del d2.skills.python
            with self.assertRaises(KeyError):
                d1.name
            with self.assertRaises(KeyError):
                d2.skills.python
        else:
            with self.assertRaises(PermissionError):
                del d1.name
            with self.assertRaises(PermissionError):
                del d2.skills.python


# Test-factory for test all combinations of permissions
for change, add, delete in product([False, True], repeat=3):
    name = ["Edit", "Add", "Del"]
    class_name = "TestPermissions_" + "".join(compress(name, [change, add, delete]))

    # save variable in globals, in order to Unittests runner can see this
    attrs = {"permissions": dict(change=change, add=add, delete=delete)}
    globals()[class_name] = type(class_name, (FactoryReadableTest,), attrs)
