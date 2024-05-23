
from .wrapper_abc import Wrapper

from typing import Any, Union

def wrapper_factory(value: Any):
  """NOTE: In order to actually use this, i would need to edit all the overloads that rely on calling __class__(ret) to dynamically
  return wrapper instances."""
  pass
