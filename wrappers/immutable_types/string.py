import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_abc import Wrapper

from collections import UserString
from typing import Any, Union


class StringWrapper(UserString, Wrapper):
    def __init__(self, value):
        self.data = value

    def to(self, new_value: Union[str, Wrapper, Any]) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.data = new_value
        return self

    def resolve(self) -> str:
        return self.data
