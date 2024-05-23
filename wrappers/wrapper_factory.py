import json
import torch
import numpy as np
from PIL import Image

from collections import deque, ChainMap, Counter
from .wrapper_abc import Wrapper
from .immutable_types.none import NoneWrapper
from .immutable_types.number import NumberWrapper
from .immutable_types.tuple import TupleWrapper
from .immutable_types.bytes import BytesWrapper
from .immutable_types.string import StringWrapper
from .external_types.tensor import TensorWrapper
from .external_types.model import ModelWrapper
from .mutable_types.dict import DictWrapper
from .mutable_types.list import ListWrapper
from .mutable_types.set import SetWrapper
from .mutable_types.deque import DequeWrapper
from .mutable_types.bytearray import ByteArrayWrapper
from .external_types.abstract_external import AbstractExternalWrapper

from typing import Any

class WrapperFactory:
  """NOTE: Careful of overloads that rely on calling __class__(value) to dynamically
  return wrapper instances."""
  def __new__(cls, data: Any) -> Wrapper:
    return cls.create_wrapper(data)

  @staticmethod
  def create_wrapper(data: Any) -> Wrapper:
    while isinstance(data, Wrapper):
      data = data.resolve()

    # Immutables
    if data is None:
      return NoneWrapper(data)
    elif isinstance(data, (int, float, complex)):
      return NumberWrapper(data)
    elif isinstance(data, tuple):
      return TupleWrapper(data)
    elif isinstance(data, bytes):
      return BytesWrapper(data)
    elif isinstance(data, str):
      try:
        deserialized = json.loads(data)
        if isinstance(deserialized, dict):
          return DictWrapper(deserialized)
        elif isinstance(deserialized, list):
          return ListWrapper(deserialized)
      except json.JSONDecodeError:
        return StringWrapper(data)
      return StringWrapper(data)
    
    # External types
    elif isinstance(data, (torch.Tensor, np.ndarray, Image.Image)):
      return TensorWrapper(data)
    elif isinstance(data, torch.nn.Module):
      return ModelWrapper(data)
    
    # Mutables
    elif isinstance(data, (dict, ChainMap, Counter)):
      return DictWrapper(data)
    elif isinstance(data, list):
      return ListWrapper(data)
    elif isinstance(data, set):
      return SetWrapper(data)
    elif isinstance(data, deque):
      return DequeWrapper(data)
    elif isinstance(data, bytearray):
      return ByteArrayWrapper(data)
    
    return AbstractExternalWrapper(data)
