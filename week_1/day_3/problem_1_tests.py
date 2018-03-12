from unittest import TestCase

from .problem_1 import sum_of_keys


class Problem1Tests(TestCase):

    def test_simple_dict(self):
        inp = [{"id": 1, "u": 1},
               {"id": 1, "u": 2}]
        out = [{"key": "id", "value": 1, "count": 2},
               {"key": "u", "value": 1, "count": 1},
               {"key": "u", "value": 2, "count": 1}]

        self.assertListEqual(sum_of_keys(inp), out)

    def test_different(self):
        inp = [{"id": 1, "u": 1},
               {"id": 2, "u": 2}]
        out = [{"key": "id", "value": 1, "count": 1},
               {"key": "u", "value": 1, "count": 1},
               {"key": "id", "value": 2, "count": 1},
               {"key": "u", "value": 2, "count": 1}]

        self.assertListEqual(sum_of_keys(inp), out)

    def test_equal(self):
        inp = [{"id": 1, "u": 1},
               {"id": 1, "u": 1}]
        out = [{"key": "id", "value": 1, "count": 2},
               {"key": "u", "value": 1, "count": 2}]

        self.assertListEqual(sum_of_keys(inp), out)
