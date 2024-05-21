import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_interface import Wrapper
from collections import UserDict


class DictWrapper(UserDict, Wrapper):
    def __init__(self, value):
        if value is None:
            self.data = {}
        else:
            self.data = dict(value)

    def to(self, new_value):
        self.data = dict(new_value)

    def resolve(self):
        return self.data
