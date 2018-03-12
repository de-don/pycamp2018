from unittest import TestCase

from .problem_2 import merge_dicts


class Problem1Tests(TestCase):

    def test_example(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 3, "c": 4}
        out = {'a': 1, 'b': 2, 'c': 4}
        self.assertDictEqual(merge_dicts(d1, d2), out)

    def test_empty_both(self):
        d1 = {}
        d2 = {}
        out = {}
        self.assertDictEqual(merge_dicts(d1, d2), out)

    def test_one_empty(self):
        d1 = {}
        d2 = {"a": 1, "b": 2}
        self.assertDictEqual(merge_dicts(d1, d2), d2)

        d1 = {"a": 1, "b": 2}
        d2 = {}
        self.assertDictEqual(merge_dicts(d1, d2), d1)

    def test_different(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        out = {"a": 1, "b": 2, "c": 3, "d": 4}
        self.assertDictEqual(merge_dicts(d1, d2), out)
