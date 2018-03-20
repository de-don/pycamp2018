from unittest import TestCase

from problem_5.factory import dict_factory
from problem_5.main_tests import (
    SimpleDictTest,
    EditableDictTest,
    ExpandableDictTest,
    RemovableDictTest,
)

dict_1 = {'name': 'Denis', 'age': 22}
dict_2 = {
    'name': 'Denis',
    'age': 22,
    'skills': {
        'python': 'middle',
        'fortran': 'lower',
    }
}

SimpleDictTest.cls = dict_factory("SimpleDict")
EditableDictTest.cls = dict_factory("EditableDict", change=True)
ExpandableDictTest.cls = dict_factory("ExpandableDict", change=True, add=True)
RemovableDictTest.cls = dict_factory("RemovableDict", change=True, add=True,
                                delete=True)


class EditableRemovableTest(TestCase):
    cls = dict_factory("EditableRemovable", change=True, delete=True)

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
        d = self.cls(dict_1)
        # try to edit already exist attr
        d.name = 'Joan'
        self.assertEqual(d.name, 'Joan')

        d = self.cls(dict_2)
        # try to edit already exist attr
        d.skills.python = 'guru'
        self.assertEqual(d.skills.python, 'guru')

    def test_add(self):
        d = self.cls(dict_1)
        # try to add new attr
        with self.assertRaises(PermissionError):
            d.title = 'example'
            self.assertEqual(d.title, 'example')

        d = self.cls(dict_2)
        # try to add new attr
        with self.assertRaises(PermissionError):
            d.skills.cpp = 'guru'
            self.assertEqual(d.skills.cpp, 'guru')

    def test_delete(self):
        d = self.cls(dict_1)
        # try to delete
        del d.name
        with self.assertRaises(KeyError):
            d.name

        d = self.cls(dict_2)
        # try to delete
        del d.skills.python
        with self.assertRaises(KeyError):
            d.python
