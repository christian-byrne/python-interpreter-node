import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_abc import Wrapper

from typing import Any, Union


class NumberWrapper(Wrapper):
    def __init__(self, value):
        self.set_value(value)

    def set_value(self, value: Union[int, float, complex, str]) -> None:
        if isinstance(value, int):
            self.data = int(value)
        elif isinstance(value, float):
            self.data = float(value)
        elif isinstance(value, complex):
            self.data = complex(value)
        elif isinstance(value, str):
            self.data = self.set_number_type_from_str(value)

        if "real" in dir(self.data):
            self.real = self.data.real
        if "imag" in dir(self.data):
            self.imag = self.data.imag
        if "numerator" in dir(self.data):
            self.numerator = self.data.numerator
        if "denominator" in dir(self.data):
            self.denominator = self.data.denominator

    def set_number_type_from_str(self, num_str: str) -> Union[int, float, complex, str]:
        try:
            float(num_str)
            return float(num_str)
        except ValueError:
            pass
        try:
            int(num_str)
            return int(num_str)
        except ValueError:
            pass
        try:
            complex(num_str)
            return complex(num_str)
        except ValueError:
            pass
        
        if num_str.startswith("0x"):
            return int(num_str, 16)
        elif num_str.startswith("0o"):
            return int(num_str, 8)
        elif num_str.startswith("0b"):
            return int(num_str, 2)
        elif num_str in ["inf", "infinity"]:
            return float("inf")
        
        return num_str

    def to(self, new_value: Union[Wrapper, Any]) -> Wrapper:
        while isinstance(new_value, Wrapper):
            new_value = new_value.resolve()

        self.set_value(new_value)
        return self

    def resolve(self) -> Union[int, float, complex]:
        return self.data

    # the follow overloaded inherited methods are defined in alphabetical order:

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

    def __bool__(self):
        return bool(self.data)

    def __ceil__(self):
        return self.data.ceil()

    def __delattr__(self, name):
        return self.data.__delattr__(name)

    def __dir__(self):
        return dir(self.data)

    def __divmod__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(divmod(self.data, other.data))
        return self.__class__(divmod(self.data, other))

    def __eq__(self, other):
        if isinstance(other, Wrapper):
            return self.data == other.data
        return self.data == other

    def __float__(self):
        return float(self.data)

    def __floor__(self):
        return self.data.floor()

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

    def __getnewargs__(self):
        return (self.data[:],)

    def __getstate__(self):
        return self.data.__getstate__()

    def __gt__(self, other):
        if isinstance(other, Wrapper):
            return self.data > other.data
        return self.data > other

    def __hash__(self):
        return hash(self.data)

    def __index__(self):
        return self.data.__index__()

    def __int__(self):
        return int(self.data)

    def __invert__(self):
        return ~self.data

    def __le__(self, other):
        if isinstance(other, Wrapper):
            return self.data <= other.data
        return self.data <= other

    def __lshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data << other.data)
        return self.__class__(self.data << other)

    def __lt__(self, other):
        if isinstance(other, Wrapper):
            return self.data < other.data
        return self.data < other

    def __mod__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data % other.data)
        return self.__class__(self.data % other)

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
        if isinstance(other, str):
            return self.__class__(float(other) + self.data)
        return self.__class__(other + self.data)

    def __rand__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data & self.data)
        return self.__class__(other & self.data)

    def __rdivmod__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(divmod(other.data, self.data))
        return self.__class__(divmod(other, self.data))

    def __reduce__(self):
        return self.data.__reduce__()

    def __reduce_ex__(self, protocol):
        return self.data.__reduce_ex__(protocol)

    def __repr__(self):
        return repr(self.data)

    def __rfloordiv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data // self.data)
        return self.__class__(other // self.data)

    def __rlshift__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(other.data << self.data)
        return self.__class__(other << self.data)

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

    def __round__(self, ndigits=None):
        return self.data.__round__(ndigits)

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

    def __sizeof__(self):
        return self.data.__sizeof__()

    def __str__(self):
        return str(self.data)

    def __sub__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data - other.data)
        elif isinstance(other, str):
            return self.__class__(self.data - float(other))
        return self.__class__(self.data - other)

    def __truediv__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data / other.data)
        return self.__class__(self.data / other)

    def __trunc__(self):
        return self.data.__trunc__()

    def __xor__(self, other):
        if isinstance(other, Wrapper):
            return self.__class__(self.data ^ other.data)
        return self.__class__(self.data ^ other)

    # the following named methods are defined in alphabetical order:

    def as_integer_ratio(self):
        return self.data.as_integer_ratio()

    def bit_count(self):
        return self.data.bit_count()

    def bit_length(self):
        return self.data.bit_length()

    def conjugate(self):
        return self.__class__(self.data.conjugate())

    def from_bytes(self, bytes, byteorder, *, signed=False):
        return self.__class__(int.from_bytes(bytes, byteorder, signed))

    def to_bytes(self, length, byteorder, *, signed=False):
        return self.data.to_bytes(length, byteorder, signed)
