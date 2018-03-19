
class SimpleDict:
    def __init__(self, input_dict):
        self.__values = dict()
        for key, value in input_dict.items():
            if isinstance(value, dict):
                value = SimpleDict(value)

            self.__values[key] = value

    def __setattr__(self, key, value):
        if key != '_SimpleDict__values':
            if key in self.__values:
                raise PermissionError
            raise KeyError
        super().__setattr__(key, value)

    def __getattr__(self, item):
        if item not in self.__values:
            raise KeyError
        return self.__values[item]
