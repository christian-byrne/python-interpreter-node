import sys
import os
import json
import torch
from collections import UserList

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrapper_abc import Wrapper
from .dict_wrapper import DictWrapper
from .number_wrapper import NumberWrapper
from .image_tensor_wrapper import TensorWrapper
from .string_wrapper import StringWrapper

from typing import Any, Union


class ListWrapper(UserList, Wrapper):
    def __init__(self, value):
        while isinstance(value, Wrapper):
            value = value.resolve()

        if isinstance(value, (list, UserList)):
            self.data = value
        elif value is None or value == []:
            self.data = []
        elif isinstance(value, (dict, bytes, bytearray)):
            self.data = DictWrapper(value)
        elif isinstance(value, (int, float, complex)):
            self.data = NumberWrapper(value)
        elif isinstance(value, torch.Tensor):
            self.data = TensorWrapper(value)
        elif isinstance(value, str):
            try:
                deserialized = json.loads(value)
                if isinstance(self.data, list):
                    self.data = deserialized
                else:
                    self.data = DictWrapper(deserialized)
            except json.JSONDecodeError:
                self.data = StringWrapper(value)
        else:
            self.data = value

    def to(self, new_value: Union[list, Wrapper, Any]) -> Wrapper:
        self.data = list(new_value)
        return self

    def resolve(self) -> list:
        return self.data
