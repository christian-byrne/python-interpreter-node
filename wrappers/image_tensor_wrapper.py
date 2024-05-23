import torch
import numpy
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrapper_abc import Wrapper

from typing import Union, Any


class TensorWrapper(Wrapper):
    def __init__(self, tensor: Union[torch.Tensor, numpy.ndarray, Image.Image]):
        self.data = self.convert_to_tensor(tensor)

    def is_tensor(self):
        return isinstance(self.data, torch.Tensor)

    def resolve(self):
        return self.data

    def to(self, tensor: Union[torch.Tensor, Wrapper]):
        if isinstance(tensor, torch.Tensor):
            self.data = tensor
        elif isinstance(tensor, Wrapper):
            self.data = tensor.resolve()
        # TODO: If, for whatever reason, user re-assigns a variable pointing at a tensor wrapper
        #       to something like an int or another obj, we should try to create the associated wrapper
        #       if the type has one. If it's not a tensor and not primitive, raise an error.

    def convert_to_tensor(
        self, tensor: Union[torch.Tensor, numpy.ndarray, Image.Image, Any]
    ):
        if isinstance(tensor, torch.Tensor):
            return tensor
        if isinstance(tensor, numpy.ndarray):
            return torch.from_numpy(tensor)
        if isinstance(tensor, Image.Image):
            return torch.tensor(numpy.array(tensor))

        try:
            return torch.tensor(tensor)
        except Exception:
            return None

    def copy(self):
        return self.__class__(self.data.clone().detach())

    def __repr__(self):
        return f"ImageTensorWrapper({self.data})"

    def __str__(self):
        if self.data is not None:
            return f"ImageTensorWrapper(tensor.shape: {self.data.shape}, dim: {self.data.dim()}, dtype: {self.data.dtype}, device: {self.data.device})"
        return "NoneType"

    # The following apply to the tensor unless the wrapper has the attribute/key.

    def __getattr__(self, attr):
        if attr == "parent_attributes":
            return [
                "data",
                "to",
                "resolve",
                "is_tensor",
                "convert_to_tensor",
                "parent_attributes",
                "copy",
            ]
        if attr in self.parent_attributes:
            return getattr(self, attr)
        return getattr(self.data, attr)

    def __setattr__(self, attr, value):
        if attr in self.parent_attributes:
            return super().__setattr__(attr, value)
        else:
            setattr(self.data, attr, value)

    def __delattr__(self, attr):
        if attr in self.parent_attributes:
            delattr(self, attr)
        else:
            del self.data[attr]

    # The following operations act as if they are the tensor.
    # Listed in alphabetical order.

    def __abs__(self):
        return abs(self.data)

    def __add__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + float(other))
        return self.__class__(self.data + other)

    def __and__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data & other.data)
        return self.__class__(self.data & other)

    def __array__(self):
        return self.data.__array__()

    def __array_priority__(self):
        return self.data.__array_priority__()

    def __array_wrap__(self):
        return self.data.__array_wrap__()

    def __bool__(self):
        return bool(self.data)

    def __complex__(self):
        return complex(self.data)

    def __contains__(self, item):
        return item in self.data

    def __deepcopy__(self, memo):
        return self.data.__deepcopy__(memo)

    def __delitem__(self, key):
        del self.data[key]

    def __dict__(self):
        return self.data.__dict__()

    def __dir__(self):
        return dir(self.data)

    def __div__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data / other.data)
        return self.__class__(self.data / other)

    def __dlpack__(self):
        return self.data.__dlpack__()

    def __dlpack_device__(self):
        return self.data.__dlpack_device__()

    def __eq__(self, other):
        if isinstance(other, Wrapper):
            return self.data == other.data
        return self.data == other

    def __float__(self):
        return float(self.data)

    def __floordiv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data // other.data)
        return self.__class__(self.data // other)

    def __format__(self, format_spec):
        return self.data.__format__(format_spec)

    def __ge__(self, other):
        if isinstance(other, Wrapper):
            return self.data >= other.data
        return self.data >= other

    def __getitem__(self, key):
        return self.data[key]

    def __getstate__(self):
        return self.data.__getstate__()

    def __gt__(self, other):
        if isinstance(other, Wrapper):
            return self.data > other.data
        return self.data > other

    def __hash__(self):
        return hash(self.data)

    def __iadd__(self, other):
        if isinstance(other, Wrapper):
            self.data += other.data
        else:
            self.data += other
        return self

    def __iand__(self, other):
        if isinstance(other, Wrapper):
            self.data &= other.data
        else:
            self.data &= other
        return self

    def __idiv__(self, other):
        if isinstance(other, Wrapper):
            self.data /= other.data
        else:
            self.data /= other
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Wrapper):
            self.data //= other.data
        else:
            self.data //= other
        return self

    def __ilshift__(self, other):
        if isinstance(other, Wrapper):
            self.data <<= other.data
        else:
            self.data <<= other
        return self

    def __imod__(self, other):
        if isinstance(other, Wrapper):
            self.data %= other.data
        else:
            self.data %= other
        return self

    def __imul__(self, other):
        if isinstance(other, Wrapper):
            self.data *= other.data
        else:
            self.data *= other
        return self

    def __index__(self):
        return self.data.__index__()

    def __int__(self):
        return int(self.data)

    def __invert__(self):
        return ~self.data

    def __ior__(self, other):
        if isinstance(other, Wrapper):
            self.data |= other.data
        else:
            self.data |= other
        return self

    def __ipow__(self, other):
        if isinstance(other, Wrapper):
            self.data **= other.data
        else:
            self.data **= other
        return self

    def __irshift__(self, other):
        if isinstance(other, Wrapper):
            self.data >>= other.data
        else:
            self.data >>= other
        return self

    def __isub__(self, other):
        if isinstance(other, Wrapper):
            self.data -= other.data
        else:
            self.data -= other
        return self

    def __iter__(self):
        return iter(self.data)

    def __itruediv__(self, other):
        if isinstance(other, Wrapper):
            self.data /= other.data
        else:
            self.data /= other
        return self

    def __ixor__(self, other):
        if isinstance(other, Wrapper):
            self.data ^= other.data
        else:
            self.data ^= other
        return self

    def __le__(self, other):
        if isinstance(other, Wrapper):
            return self.data <= other.data
        return self.data <= other

    def __len__(self):
        return len(self.data)

    def __long__(self):
        return long(self.data)

    def __lshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data << other.data)
        return self.__class__(self.data << other)

    def __lt__(self, other):
        if isinstance(other, Wrapper):
            return self.data < other.data
        return self.data < other

    def __matmul__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data @ other.data)
        return self.__class__(self.data @ other)

    def __mod__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data % other.data)
        return self.__class__(self.data % other)

    def __module__(self):
        return self.data.__module__()

    def __mul__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data * other.data)
        return self.__class__(self.data * other)

    def __ne__(self, other):
        if isinstance(other, Wrapper):
            return self.data != other.data
        return self.data != other

    def __neg__(self):
        return -self.data

    def __nonzero__(self):
        return self.data.__nonzero__()

    def __or__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data | other.data)
        return self.__class__(self.data | other)

    def __pos__(self):
        return +self.data

    def __pow__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data**other.data)
        return self.__class__(self.data**other)

    def __radd__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data + self.data)
        return self.__class__(other + self.data)

    def __rand__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data & self.data)
        return self.__class__(other & self.data)

    def __rdiv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data / self.data)
        return self.__class__(other / self.data)

    def __reduce__(self):
        return self.data.__reduce__()

    def __reduce_ex__(self, protocol):
        return self.data.__reduce_ex__(protocol)

    def __reversed__(self):
        return reversed(self.data)

    def __rfloordiv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data // self.data)
        return self.__class__(other // self.data)

    def __rlshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data << self.data)
        return self.__class__(other << self.data)

    def __rmatmul__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data @ self.data)
        return self.__class__(other @ self.data)

    def __rmod__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data % self.data)
        return self.__class__(other % self.data)

    def __rmul__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data * self.data)
        return self.__class__(other * self.data)

    def __ror__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data | self.data)
        return self.__class__(other | self.data)

    def __rpow__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data**self.data)
        return self.__class__(other**self.data)

    def __rrshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data >> self.data)
        return self.__class__(other >> self.data)

    def __rshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data >> other.data)
        return self.__class__(self.data >> other)

    def __rsub__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data - self.data)
        return self.__class__(other - self.data)

    def __rtruediv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data / self.data)
        return self.__class__(other / self.data)

    def __rxor__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data ^ self.data)

        return self.__class__(other ^ self.data)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __setstate__(self, state):
        self.data.__setstate__(state)

    def __sizeof__(self):
        return self.data.__sizeof__()

    def __sub__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data - other.data)
        return self.__class__(self.data - other)

    def __torch_dispatch__(self):
        return self.data.__torch_dispatch__()

    def __torch_function__(self):
        return self.data.__torch_function__()

    def __truediv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data / other.data)
        return self.__class__(self.data / other)

    def __weakref__(self):
        return self.data.__weakref__()

    def __xor__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data ^ other.data)
        return self.__class__(self.data ^ other)
