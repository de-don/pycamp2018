import csv
import sqlite3

with open('input.csv', 'r') as file:
    reader = csv.reader(file, delimiter=";")
    head = list(next(reader))
    lines = list(reader)

if not (head and lines):
    raise Exception

colnames = ','.join(head)

con = sqlite3.connect('input.db')
cur = con.cursor()
cur.execute("CREATE TABLE test_table (%s);" % colnames)

cur.executemany(
    "INSERT INTO test_table (%s) VALUES (%s);" % (
        colnames,
        ', '.join('?' * len(head))
    )
    , lines)
con.commit()
con.close()
