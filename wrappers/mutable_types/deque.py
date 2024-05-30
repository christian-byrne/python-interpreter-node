import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_abc import Wrapper

from collections import deque
from typing import Union, Any


class DequeWrapper(Wrapper, deque):
    def __init__(self, value: deque):
        self.data = value

    def to(self, new_value: Union[deque, Wrapper, Any]) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.data = new_value
        return self

    def resolve(self) -> deque:
        return self.data
