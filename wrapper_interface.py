from abc import ABC, abstractmethod
from typing import Any, Union
import torch


class Wrapper(ABC):
    @abstractmethod
    def to(self, tensor) -> None:
        pass

    @abstractmethod
    def resolve(self) -> Union[torch.Tensor, Any]:
        pass
