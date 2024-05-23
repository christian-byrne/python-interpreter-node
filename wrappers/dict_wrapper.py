import sys
import os
import json
import torch
from collections import UserDict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrapper_abc import Wrapper
from .list_wrapper import ListWrapper
from .number_wrapper import NumberWrapper
from .string_wrapper import StringWrapper
from .image_tensor_wrapper import TensorWrapper

from typing import Any, Union


class DictWrapper(UserDict, Wrapper):
    def __init__(self, value):
        while isinstance(value, Wrapper):
            value = value.resolve()

        if isinstance(value, (dict, UserDict)):
            self.data = value
        elif value is None or value == {}:
            self.data = {}
        elif isinstance(value, list):
            self.data = ListWrapper(value)
        elif isinstance(value, (int, float, complex)):
            self.data = NumberWrapper(value)
        elif isinstance(value, torch.Tensor):
            self.data = TensorWrapper(value)
        elif isinstance(value, str):
            try:
                self.data = json.loads(value)
            except json.JSONDecodeError:
                self.data = StringWrapper(value)
        else:
            self.data = value

    def to(self, new_value: Union[dict, Wrapper, Any]) -> Wrapper:
        self.data = dict(new_value)
        return self

    def resolve(self) -> dict:
        return self.data
