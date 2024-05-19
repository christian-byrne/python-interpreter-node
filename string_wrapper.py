import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .wrapper_interface import Wrapper
from collections import UserString

class StringWrapper(UserString, Wrapper):
    def __init__(self, value):
        self.data = str(value)

    def to(self, new_value):
        self.data = str(new_value)

    def resolve(self):
        return self.data