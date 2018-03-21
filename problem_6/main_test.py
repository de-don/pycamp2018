from unittest import TestCase

from problem_6.main import Table


class TableTest(TestCase):

    def setUp(self):
        self.input = {'csv': 'input.csv'}

    def test_init_from_csv(self):
        data = Table.from_csv(self.input['csv'])
        result = "\n".join([
            "0:",
            "    name: john",
            "    birthday: 1988-12-12",
            "    salary: 100",
            "1:",
            "    name: kevin",
            "    birthday: 1972-12-12",
            "    salary: 200",
            "2:",
            "    name: barney",
            "    birthday: 1972-12-12",
            "    salary: 300",
        ])

        self.assertEqual(str(data), result)

    def test_method_count(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.count(), 3)

    def test_method_sum(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.sum('salary'), 600)

    def test_method_avg(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.avg('salary'), 200)

    def test_method_headers(self):
        data = Table.from_csv(self.input['csv'])
        headers = data.headers
        result = ['name', 'birthday', 'salary']
        self.assertListEqual(headers, result)

    def test_method_get_row(self):
        data = Table.from_csv(self.input['csv'])
        data_row_0 = ["name: john", "birthday: 1988-12-12", "salary: 100"]
        self.assertEqual(str(data[0]), '\n'.join(data_row_0))
        with self.assertRaises(TypeError):
            data['first']

    def test_method_unique(self):
        data = Table.from_csv(self.input['csv'])
        self.assertSetEqual(data.unique('salary'), {100, 200, 300})
        self.assertSetEqual(data.unique('name'), {'john', 'kevin', 'barney'})
        self.assertSetEqual(
            data.unique('birthday'),
            {'1988-12-12', '1972-12-12'},
        )
