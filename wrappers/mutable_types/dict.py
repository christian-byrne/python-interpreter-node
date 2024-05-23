import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_abc import Wrapper

from collections import UserDict
from typing import Any, Union


class DictWrapper(UserDict, Wrapper):
    def __init__(self, value):
        self.data = value

    def to(self, new_value: Union[dict, Wrapper, Any]) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.data = dict(new_value)
        return self

    def resolve(self) -> dict:
        return self.data
