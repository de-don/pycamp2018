class BaseDict:
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
        if item not in self.__dict__:
            raise KeyError(f'Key {item} not found in dict')
        raise PermissionError


class EditMixin:
    def __setattr__(self, key, value):
        if key not in self.__dict__:
            # key doesn't exists, need to add
            super().__setattr__(key, value)
        self.__dict__[key] = value


class AddMixin:
    def __setattr__(self, key, value):
        if key in self.__dict__:
            # key already exists, not need to add
            super().__setattr__(key, value)
        self.__dict__[key] = value


class DelMixin:
    def __delattr__(self, item):
        if item not in self.__dict__:
            # key doesn't exists
            super().__delattr__(item)
        del self.__dict__[item]


def factory(class_name, change=False, add=False, delete=False):
    bases = [BaseDict]
    if change:
        bases.insert(0, EditMixin)
    if add:
        bases.insert(0, AddMixin)
    if delete:
        bases.insert(0, DelMixin)

    bases = tuple(bases)
    return type(class_name, bases, {})
