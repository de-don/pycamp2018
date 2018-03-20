from itertools import compress
from collections import defaultdict


class ProtectedError(PermissionError):
    """ Error caused by actions with protected attributes. """
    pass


class BaseDict:
    """ Сlass for storing a dict and accessing its elements through attrs.

    Raises:
        PermissionError: You don't have permissions to this action.
        KeyError: element with this key not found in dict
    """

    def __init__(self, input_dict, *args, **kwargs):
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
    """ Mixin which allow to edit a values by attribute. """

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
    """ Mixin which allow to delete only exist attribute. """

    def __delattr__(self, item):
        if item not in self.__dict__:
            # key doesn't exists
            return super().__delattr__(item)
        del self.__dict__[item]


class ProtectedMixin:
    """ Mixin which allow to protect attributes.

     Protected attribute is forbidden to change and delete.
     If you try it, you get 'ProtectedError'.
     """
    __protected = []

    def __init__(self, input_dict, protected):
        self.__set_protected(protected)

        cls = self.__class__
        for key, value in input_dict.items():
            # if value is dict, create new instance
            if isinstance(value, dict):
                value = cls(value, protected=self.__protected.get(key, []))
            # save key:value
            self.__dict__[key] = value

    def __set_protected(self, protected):
        """ Method to set process input list of attr names.

        Method create dict of lists, where key - it is main-attribute name,
        and key it is list of his sub-attributes or [''], if is simple
        attribute. This dict set to self.protected for future using.

        Args:
             protected(List[str]): list of attr names, such as 'attr.subattr'
        """

        protected_filtered = defaultdict(list)
        # filtering protected params
        for item in protected:
            parts = item.split(".")
            if not parts:
                continue
            main_attr = parts[0]
            sub_attr = ".".join(parts[1:])
            protected_filtered[main_attr].append(sub_attr)
        self.__protected = protected_filtered

    def __setattr__(self, key, value):
        if key not in self.__protected:
            return super().__setattr__(key, value)
        raise ProtectedError("this attribute is forbidden")

    def __delattr__(self, item):
        if item not in self.__protected:
            return super().__delattr__(item)
        raise ProtectedError("this attribute is forbidden")


def dict_factory(class_name, change=False, add=False, delete=False,
                 protected=False):
    """ Function to create class with selected permissions.

    Args:
        class_name(str): Future class name
        change(bool): true, if have permission to change exists keys.
        add(bool): True, if have permission to add new keys.
        delete(bool): True, if have permission to delete exists keys.
        protected(bool): True, if dict must have protected attrs.

    Returns:
        class: New class for storing dict with selected permissions.
    """
    bases = [ProtectedMixin, DelMixin, AddMixin, EditMixin, BaseDict]
    flags = [protected, delete, add, change, True]
    bases = compress(bases, flags)

    return type(class_name, tuple(bases), {})
