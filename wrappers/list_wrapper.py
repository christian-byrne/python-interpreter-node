import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ..wrapper_interface import Wrapper
from collections import UserList


class ListWrapper(UserList, Wrapper):
    def __init__(self, value):
        if value is None:
            self.data = []
        else:
            self.data = list(value)

    def to(self, new_value):
        self.data = list(new_value)

    def resolve(self):
        return self.data
