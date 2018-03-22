class SimpleDict(dict):
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


class EditableDict(SimpleDict):
    def __setattr__(self, key, value):
        if self.get(key, None):
            self[key] = value
            return
        super().__setattr__(key, value)


class ExpandableDict(EditableDict):
    def __setattr__(self, key, value):
        self[key] = value


class RemovableDict(ExpandableDict):
    def __delattr__(self, item):
        del self[item]
