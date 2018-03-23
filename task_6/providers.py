import csv
import json
import sqlite3
from collections import OrderedDict

import yaml


class CsvProvider:
    def __init__(self, config):
        self.file_path = config.get('file_path')
        self.delimiter = config.get('delimiter', ';')

    def get_data(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file, delimiter=self.delimiter)
            return next(reader), list(reader)

    def save_data(self, head, lines):
        with open(self.file_path, 'w') as file:
            writer = csv.writer(file, delimiter=self.delimiter)
            writer.writerow(head)
            writer.writerows(lines)


class JsonProvider:
    def __init__(self, config):
        self.file_path = config.get('file_path')

    def get_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            head = list(data.keys())
            columns = data.values()
            rows_count = len(data[head[0]])
            lines = (
                (column[i] for column in columns)
                for i in range(rows_count)
            )
            return head, lines

    def save_data(self, head, lines):
        # convert list of map to list of list
        lines = [list(row) for row in lines]
        dictionary = {
            col_name: [str(row[i]) for row in lines]
            for i, col_name in enumerate(head)
        }

        with open(self.file_path, 'w') as file:
            json.dump(dictionary, file)


class Sqlite3Provider:
    def __init__(self, config):
        self.file_path = config.get('file_path')
        self.table_name = config.get('table_name')

    def get_data(self):
        with sqlite3.connect(self.file_path) as con:
            data = con.execute('PRAGMA table_info(%s);' % self.table_name)
            head = (row[1] for row in data)
            lines = con.execute('SELECT * FROM %s;' % self.table_name)
            return head, lines


class HtmlProvider:
    def __init__(self, config):
        self.file_path = config.get('file_path')

    def save_data(self, head, lines):
        table = '<table><thead>\n{thead}\n</thead>' \
                '<tbody>\n{tbody}\n</tbody></table>'

        tr = '  <tr>\n{item}\n  </tr>'
        td = '    <td>{item}</td>'
        th = '  <th>{item}</th>'

        th_items = (th.format(item=col_name) for col_name in head)

        def tr_items():
            for row in lines:
                td_items = (td.format(item=cell) for cell in row)
                yield tr.format(item='\n'.join(td_items))

        text = table.format(
            thead='\n'.join(th_items),
            tbody='\n'.join(tr_items())
        )

        with open(self.file_path, 'w') as file:
            file.write(text)


class YamlProvider:
    def __init__(self, config):
        self.file_path = config.get('file_path')

    def get_data(self):
        with open(self.file_path, 'r') as file:
            lines = yaml.load(file)
            head = lines[0].keys()
            rows = (
                [line[col_name] for col_name in head]
                for line in lines
            )
            return head, rows

    def save_data(self, head, lines):
        with open(self.file_path, 'w') as file:
            items = [
                OrderedDict(zip(head, line))
                for line in lines
            ]
            yaml.dump(items, file, default_flow_style=False)