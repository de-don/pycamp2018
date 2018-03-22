from collections import defaultdict
from copy import deepcopy


class ProtectedError(PermissionError):
    """ Error caused by actions with protected attributes. """
    pass


class BaseDict:
    """ Сlass for storing a dict and accessing its elements through attrs.

    Raises:
        PermissionError: You don't have permissions to this action.
        KeyError: element with this key not found in dict
    """
    _protected = {}

    def __init__(self, input_dict):
        if not isinstance(input_dict, dict):
            raise TypeError('input_dict must be instance dict.')
        for key, value in input_dict.items():
            self._add(key, value)

    def _add(self, key, value):
        # if value is dict, create new instance
        if isinstance(value, dict):
            value = self.__class__(value)
        else:
            value = deepcopy(value)
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


##################################################
# protected
##################################################

def protected_add(self, key, value):
    # if value is dict, create new instance
    if isinstance(value, dict):
        protected_attributes = self._protected.get(key, None)
        value = self.__class__(value, protected=protected_attributes)
    else:
        value = deepcopy(value)
    self.__dict__[key] = value


def protected_set_protected(self, protected):
    protected_filtered = defaultdict(list)
    # filtering protected params
    for item in protected:
        parts = item.split(".", 1)
        if not parts:
            continue
        main_attr = parts[0]
        sub_attr = parts[1] if len(parts) == 2 else ''
        protected_filtered[main_attr].append(sub_attr)
    self.__dict__['_protected'] = protected_filtered


###############################################################################

def dict_factory(class_name, change=False, add=False, delete=False,
                 protect=False):
    """ Function to create class with selected permissions.

    Args:
        class_name(str): Future class name
        change(bool): true, if have permission to change exists keys.
        add(bool): True, if have permission to add new keys.
        delete(bool): True, if have permission to delete exists keys.
        protect(bool): True, if dict must have protected attrs.

    Returns:
        class: New class for storing dict with selected permissions.
    """

    def my__setattr__(self, key, value):
        if key not in self._protected:
            if add and key not in self.__dict__:
                self.__dict__[key] = value
                return
            if change and key in self.__dict__:
                self.__dict__[key] = value
                return
            return super(self.__class__, self).__setattr__(key, value)

        if protect and key in self._protected:
            raise ProtectedError("this attribute is forbidden")
        super(self.__class__, self).__setattr__(key, value)

    def my__delattr__(self, item):
        if item not in self.__dict__:
            # key doesn't exists
            return super(self.__class__, self).__delattr__(item)
        if item in self._protected:
            raise ProtectedError("this attribute is forbidden")
        if delete:
            # allow delete exists keys
            del self.__dict__[item]
            return
        return super(self.__class__, self).__delattr__(item)

    attrs = {
        '__setattr__': my__setattr__,
        '__delattr__': my__delattr__,
    }

    if protect:
        attrs['_add'] = protected_add
        attrs['_set_protected'] = protected_set_protected

        def my__init__(self, input_dict, protected=None):
            self._set_protected(protected if protected else [])
            super(self.__class__, self).__init__(input_dict)

        attrs['__init__'] = my__init__

    return type(class_name, (BaseDict,), attrs)
