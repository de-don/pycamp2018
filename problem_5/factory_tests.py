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
