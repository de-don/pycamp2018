""" simple script for export csv to sqlite3 """

import csv
import sqlite3

with open('input.csv', 'r') as file:
    reader = csv.reader(file, delimiter=";")
    head = list(next(reader))
    lines = list(reader)

if not (head and lines):
    raise Exception

col_names = ','.join(head)

with sqlite3.connect('input.db') as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE test_table (%s);" % col_names)

    cur.executemany(
        "INSERT INTO test_table (%s) VALUES (%s);" % (
            col_names,
            ', '.join('?' * len(head))
        )
        , lines)
    con.commit()
    con.close()
