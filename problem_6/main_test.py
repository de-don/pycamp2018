import datetime
import os
import tempfile
from unittest import TestCase

from problem_6.main import NotSupported, Table


class TableTest(TestCase):

    def setUp(self):
        self.input = {
            'csv': 'inputs/input.csv',
            'json': 'inputs/input.json',
            'sqlite3': 'inputs/input.db',
        }

        self.init_result = '\n'.join([
            '0:',
            '    name: john',
            '    birthday: 1988-12-12 00:00:00',
            '    salary: 100',
            '1:',
            '    name: kevin',
            '    birthday: 1972-12-12 00:00:00',
            '    salary: 200',
            '2:',
            '    name: barney',
            '    birthday: 1972-12-12 00:00:00',
            '    salary: 300',
        ])

        self.tmp_name = tempfile.mktemp()

    def test_init_from_csv(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(str(data), self.init_result)

    def test_init_from_json(self):
        data = Table.from_json(self.input['json'])
        self.assertEqual(str(data), self.init_result)

    def test_init_from_sqlite3(self):
        data = Table.from_sqlite3(self.input['sqlite3'], 'test_table')
        self.assertEqual(str(data), self.init_result)

    def test_count(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.count(), 3)

    def test_sum(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.sum('salary'), 600)

    def test_avg(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data.avg('salary'), 200)

    def test_headers(self):
        data = Table.from_csv(self.input['csv'])
        headers = data.headers
        result = ['name', 'birthday', 'salary']
        self.assertListEqual(headers, result)

    def test_get_row(self):
        data = Table.from_csv(self.input['csv'])
        data_row_0 = [
            'name: john',
            'birthday: 1988-12-12 00:00:00',
            'salary: 100'
        ]
        self.assertEqual(str(data[0]), '\n'.join(data_row_0))
        with self.assertRaises(TypeError):
            d = data['first']
            del d

    def test_unique(self):
        data = Table.from_csv(self.input['csv'])
        self.assertSetEqual(data.unique('salary'), {100, 200, 300})
        self.assertSetEqual(data.unique('name'), {'john', 'kevin', 'barney'})

    def test_columns_one(self):
        data = Table.from_csv(self.input['csv'])
        data_name = Table(
            rows=(('john',), ('kevin',), ('barney',)),
            col_names=('name',)
        )
        self.assertEqual(data.columns('name'), data_name)

    def test_columns_two(self):
        data = Table.from_csv(self.input['csv'])
        data_name_and_salary = Table(
            rows=(('john', 100), ('kevin', 200), ('barney', 300)),
            col_names=('name', 'salary')
        )
        self.assertEqual(data.columns('name', 'salary'), data_name_and_salary)

    def test_columns_two_reverse(self):
        data = Table.from_csv(self.input['csv'])
        data_salary_and_name = Table(
            rows=((100, 'john'), (200, 'kevin'), (300, 'barney')),
            col_names=('salary', 'name')
        )
        self.assertEqual(data.columns('salary', 'name'), data_salary_and_name)

    def test_get_cell_value(self):
        data = Table.from_csv(self.input['csv'])
        self.assertEqual(data[0]['name'], 'john')
        self.assertEqual(data[1]['salary'], 200)

    def test_order_by(self):
        data = Table.from_csv(self.input['csv'])
        data_order_salary = data.copy()
        data_order_salary_rev = Table(
            rows=(
                ('barney', '1972-12-12 00:00:00', 300),
                ('kevin', '1972-12-12 00:00:00', 200),
                ('john', '1988-12-12 00:00:00', 100),
            ),
            col_names=('name', 'birthday', 'salary')
        )

        self.assertEqual(data.order_by('salary'), data_order_salary)
        self.assertEqual(
            data.order_by('salary', reverse=True),
            data_order_salary_rev,
        )

    def test_filter_without_funcs_1(self):
        data = Table.from_csv(self.input['csv'])
        data_filtered = data.filter(
            salary=200,
        )
        self.assertEqual(data_filtered.count(), 1)
        self.assertEqual(data_filtered[0]['salary'], 200)
        self.assertEqual(data_filtered[0]['name'], 'kevin')

    def test_filter_without_funcs_2(self):
        data = Table.from_csv(self.input['csv'])
        d = datetime.datetime(year=1972, day=12, month=12)
        data_filtered = data.filter(
            birthday=d,
        )
        self.assertEqual(data_filtered.count(), 2)
        self.assertEqual(data_filtered[0]['birthday'], d)
        self.assertEqual(data_filtered[1]['birthday'], d)

    def test_filter_without_funcs_3(self):
        data = Table.from_csv(self.input['csv'])
        d = datetime.datetime(year=1972, day=12, month=12)
        data_filtered = data.filter(
            birthday=d,
            name='kevin'
        )
        self.assertEqual(data_filtered.count(), 1)
        self.assertEqual(data_filtered[0]['birthday'], d)
        self.assertEqual(data_filtered[0]['name'], 'kevin')

    def test_filter_not_supported_func(self):
        data = Table.from_csv(self.input['csv'])

        with self.assertRaises(NotSupported):
            d = data.filter(birthday__startswith=100)
            del d

    def test_filter_str_startswith(self):
        data = Table.from_csv(self.input['csv'])
        data_filtered = data.filter(
            name__startswith='bar',
        )
        self.assertEqual(data_filtered.count(), 1)
        self.assertTrue(
            data_filtered[0]['name'].startswith('bar')
        )

    def test_filter_str_endswith(self):
        data = Table.from_csv(self.input['csv'])
        data_filtered = data.filter(
            name__endswith='vin',
        )
        self.assertEqual(data_filtered.count(), 1)
        self.assertTrue(data_filtered[0]['name'].endswith('vin'))

    def test_filter_int_ge(self):
        data = Table.from_csv(self.input['csv'])
        data_filtered = data.filter(
            salary__ge=200,
        )
        self.assertEqual(data_filtered.count(), 2)
        self.assertTrue(data_filtered[0]['salary'] >= 200)
        self.assertTrue(data_filtered[1]['salary'] >= 200)

    def test_filter_int_gt(self):
        data = Table.from_csv(self.input['csv'])
        data_filtered = data.filter(
            salary__gt=200,
        )
        self.assertEqual(data_filtered.count(), 1)
        self.assertTrue(data_filtered[0]['salary'] > 200)

    def test_export_to_csv(self):
        data1 = Table.from_csv(self.input['csv'])
        data1.to_csv(self.tmp_name)

        data2 = Table.from_csv(self.tmp_name)
        self.assertEqual(data1, data2)
        os.remove(self.tmp_name)

    def test_export_to_json(self):
        data1 = Table.from_json(self.input['json'])
        data1.to_json(self.tmp_name)

        data2 = Table.from_json(self.tmp_name)
        self.assertEqual(data1, data2)
        os.remove(self.tmp_name)

    def test_export_to_html(self):
        data1 = Table.from_csv(self.input['csv'])
        data1.to_html(self.tmp_name)
        # don't now how check
        os.remove(self.tmp_name)
