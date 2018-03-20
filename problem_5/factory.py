class BaseDict:
    """ Сlass for storing a dict and accessing its elements through attrs.

    Raises:
        PermissionError: You don't have permissions to this action.
        KeyError: element with this key not found in dict
    """

    def __init__(self, input_dict):
        cls = self.__class__
        for key, value in input_dict.items():
            # if value is dict, create new instance
            if isinstance(value, dict):
                value = cls(value)
            # save key:value
            self.__dict__[key] = value

    def __setattr__(self, key, value):
        # Disable access to edit attributes
        raise PermissionError

    def __getattr__(self, item):
        # If attr doesn't be found
        raise KeyError(f'Key {item} not found in dict')

    def __delattr__(self, item):
        if item not in self.__dict__:
            raise KeyError(f'Key {item} not found in dict')
        # Disable access to edit attributes
        raise PermissionError


class EditMixin:
    """ Mixin which allow to edit a values by attribute """

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            # key doesn't exists, need to add
            return super().__setattr__(key, value)
        self.__dict__[key] = value


class AddMixin:
    """ Mixin which allow to set a values for only new attribute """

    def __setattr__(self, key, value):
        if key in self.__dict__:
            # key already exists, not need to add
            return super().__setattr__(key, value)
        self.__dict__[key] = value


class DelMixin:
    """ Mixin which allow to delete only exist attribute """

    def __delattr__(self, item):
        if item not in self.__dict__:
            # key doesn't exists
            return super().__delattr__(item)
        del self.__dict__[item]


def dict_factory(class_name, change=False, add=False, delete=False):
    """ Function to create class with selected permissions.

    Args:
        class_name(str): Future class name
        change(bool): true, if have permission to change exists keys.
        add(bool): True, if have permission to add new keys.
        delete(bool): True, if have permission to delete exists keys.

    Returns:
        class: New class for storing dict with selected permissions.
    """
    bases = [BaseDict]
    if change:
        bases.insert(0, EditMixin)
    if add:
        bases.insert(0, AddMixin)
    if delete:
        bases.insert(0, DelMixin)

    return type(class_name, tuple(bases), {})
