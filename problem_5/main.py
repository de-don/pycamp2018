class SimpleDict:
    """ Class for store dict and access to keys from attribute"""

    def __init__(self, input_dict):
        cls = self.__class__
        for key, value in input_dict.items():
            # if value is dict, create new instance
            if isinstance(value, dict):
                value = cls(value)
            # save key:value
            self.__dict__[key] = value

    def __setattr__(self, key, value):
        """ Disable access to edit attributes """
        raise PermissionError

    def __getattr__(self, item):
        raise KeyError(f'Key {item} not found in dict')

    def __delattr__(self, item):
        raise PermissionError


class EditableDict(SimpleDict):
    def __setattr__(self, key, value):
        if key not in self.__dict__:
            super().__setattr__(key, value)
        self.__dict__[key] = value


class ExpandableDict(EditableDict):
    def __setattr__(self, key, value):
        self.__dict__[key] = value


class RemovableDict(ExpandableDict):
    def __delattr__(self, item):
        if item not in self.__dict__:
            raise KeyError(f'Key {item} not found in dict')
        del self.__dict__[item]
