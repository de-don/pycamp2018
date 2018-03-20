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
        if item not in self.__dict__:
            raise KeyError(f'Key {item} not found in dict')
        raise PermissionError


class EditableDictMixin:
    def __setattr__(self, key, value):
        if key not in self.__dict__:
            super().__setattr__(key, value)
        self.__dict__[key] = value


class ExpandableDictMixin:
    def __setattr__(self, key, value):
        self.__dict__[key] = value


class RemovableDictMixin:
    def __delattr__(self, item):
        if item not in self.__dict__:
            super().__delattr__(item)
        del self.__dict__[item]


def factory(class_name, change=True, add=False, delete=False):
    bases = [SimpleDict, ]
    mixins = []
    if change:
        mixins.append(EditableDictMixin)
    if add:
        mixins.append(ExpandableDictMixin)
    if delete:
        mixins.append(RemovableDictMixin)

    bases = tuple(mixins[::-1] + bases)
    return type(class_name, bases, {})


EditableDict = factory("EditableDict", change=True)
ExpandableDict = factory("ExpandableDict", change=True, add=True)
RemovableDict = factory("RemovableDict", change=True, add=True, delete=True)
