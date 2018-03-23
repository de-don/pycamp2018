# problem_6

Инструмент для работы с данными, представленными в виде таблиц (CSV, JSON, sqlite3).

* **main.py** - модуль с основными классами (Table, Entry, TableDataProvider)
* **main_tests.py** - тесты для main.py
* **providers.py** - Классы для импорта/экспорта данных
* **inputs/** - папка с таблицами в разных форматах для импорта в класс.
* **\_\_init\_\_.py** - init-файл


```python
from task_6 import Table

data = Table.from_csv("inputs/input.csv")
sub_table = data.columns("name", "salary")
print(sub_table)
```