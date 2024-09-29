from collections import namedtuple

from ..wrapper_abc import Wrapper


class TupleWrapper(Wrapper):
    def __init__(self, value):
        self.data = value

    def to(self, new_value) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.data = new_value
        return self

    def resolve(self):
        return self.data

    def __getitem__(self, key):
        if key == "parent_attributes":
            return [
                "data",
                "to",
                "resolve",
                "parent_attributes",
            ]
        elif key in self.parent_attributes:
            return getattr(self, key)
        else:
            return getattr(self.data, key)

    def __setitem__(self, key, value):
        if key in self.parent_attributes:
            setattr(self, key, value)
        else:
            setattr(self.data, key, value)

    def __repr__(self):
        return f"TupleWrapper({self.data})"
