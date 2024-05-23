from collections import namedtuple

from ..wrapper_abc import Wrapper


class TupleWrapper(namedtuple("TupleWrapper", "data"), Wrapper):
    def __new__(cls, data):
        return super().__new__(cls, data)

    def to(self, new_data) -> Wrapper:
        return TupleWrapper(new_data)

    def resolve(self) -> tuple:
        return self.data
