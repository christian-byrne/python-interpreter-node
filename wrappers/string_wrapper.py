import sys
import os
import torch
from collections import UserString

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrapper_abc import Wrapper
from .list_wrapper import ListWrapper
from .dict_wrapper import DictWrapper
from .number_wrapper import NumberWrapper
from .image_tensor_wrapper import TensorWrapper

from typing import Any, Union


class StringWrapper(UserString, Wrapper):
    def __init__(self, value):
        while isinstance(value, Wrapper):
            value = value.resolve()

        if isinstance(value, str):
            self.data = value
        elif value is None:
            self.data = ""
        elif isinstance(value, (int, float, complex)):
            self.data = NumberWrapper(value)
        elif isinstance(value, list):
            self.data = ListWrapper(value)
        elif isinstance(value, (dict, bytes, bytearray)):
            self.data = DictWrapper(value)
        elif isinstance(value, torch.Tensor):
            self.data = TensorWrapper(value)
        else:
            self.data = str(value)

    def to(self, new_value: Union[str, Wrapper, Any]) -> Wrapper:
        self.data = str(new_value)
        return self

    def resolve(self) -> str:
        return self.data
