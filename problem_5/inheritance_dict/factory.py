from collections import defaultdict
from itertools import compress


class ProtectedError(PermissionError):
    """ Error caused by actions with protected attributes. """
    pass


class BaseDict(dict):
    """ Сlass for storing a dict and accessing its elements through attrs.

    Raises:
        PermissionError: You don't have permissions to this action.
        KeyError: element with this key not found in dict
    """

    def __init__(self, input_dict) -> None:
        kwargs = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                value = self.__class__(value)
            kwargs[key] = value
        super().__init__(**kwargs)

    def __getattr__(self, item):
        if self.get(item) is None:
            raise KeyError
        return self.get(item)

    def __setattr__(self, key, value):
        raise PermissionError

    def __delattr__(self, item):
        raise PermissionError


class EditMixin:
    """ Mixin which allow to edit a values by attribute. """

    def __setattr__(self, key, value):
        if self.get(key, None):
            self[key] = value
            return
        super().__setattr__(key, value)


class AddMixin:
    """ Mixin which allow to set a values for only new attribute """

    def __setattr__(self, key, value):
        if not self.get(key, None):
            self[key] = value
            return
        super().__setattr__(key, value)


class DelMixin:
    """ Mixin which allow to delete only exist attribute. """

    def __delattr__(self, item):
        del self[item]


class ProtectedMixin:
    """ Mixin which allow to protect attributes.

     Protected attribute is forbidden to change and delete.
     If you try it, you get 'ProtectedError'.
     """

    def __init__(self, input_dict, protected=None):
        protected = self._set_protected(protected if protected else [])
        kwargs = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                protected_attributes = protected.get(key, None)
                value = self.__class__(value, protected=protected_attributes)
            kwargs[key] = value
        self.__dict__['_protected'] = protected
        super(BaseDict, self).__init__(kwargs)

    @staticmethod
    def _set_protected(protected):
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
            parts = item.split(".", 1)
            if not parts:
                continue
            main_attr = parts[0]
            sub_attr = parts[1] if len(parts) == 2 else ''
            protected_filtered[main_attr].append(sub_attr)
        return protected_filtered

    def __setattr__(self, key, value):
        if key in self._protected:
            raise ProtectedError("this attribute is forbidden")
        super().__setattr__(key, value)

    def __delattr__(self, item):
        if item in self._protected:
            raise ProtectedError("this attribute is forbidden")
        super().__delattr__(item)


def dict_factory(class_name, change=False, add=False, delete=False,
                 protect=False):
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
    flags = [protect, delete, add, change, True]
    bases = compress(bases, flags)

    return type(class_name, tuple(bases), {})
