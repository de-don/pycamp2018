# task_5

Создание словарей, доступ к элементам которых возможен через соответствующие 
ключам словаря атрибуты, а так же возможность создавать словари с разными правами 
доступа.


* **factory.py** - фабрика словарей с mixins.
* **factory_tests.py** - тесты для factory.py
* **factory_tests_fab.py** - фабрика тестов для factory.py

```python
from task_5.factory import dict_factory

ProtectedDict = dict_factory(
    change=True,
    add=False,
    delete=False,
    protect=True    
)

dictionary = ProtectedDict(
    {
        "name": "Denis", 
        "age": 22, 
        "skills":{"python": "junior", "cpp":"bakalavr"},
    },
    protected=["name", "skills.cpp"]
)

dictionary.name
>> "Denis"
dictionary.skills.python
>> "junior"
dictionary.age
>> 22
dictionary.age = 23
dictionary.age
>> 23
dictionary.skills.cpp = "gupu"
>> ProtectedError
del dictionary.name
>> ProtectedError
```
