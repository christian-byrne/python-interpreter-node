from abc import ABC, abstractmethod
from typing import Any, Union, Generic, TypeVar

T = TypeVar("T")


class Wrapper(ABC, Generic[T]):
    @abstractmethod
    def to(self, new_data: Union[T, Any]) -> None:
        pass

    @abstractmethod
    def resolve(self) -> T:
        pass
