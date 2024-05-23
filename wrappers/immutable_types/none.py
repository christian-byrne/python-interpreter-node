import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_abc import Wrapper

from typing import Any, Union


class NoneWrapper(Wrapper):
    def __init__(self, value: None):
        self.data = value

    def to(self, new_value: Union[None, Wrapper, Any]) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.data = new_value
        return self

    def resolve(self) -> None:
        return self.data

    def __str__(self) -> str:
        return "None"

    def __repr__(self) -> str:
        return super().__repr__()
