from abc import ABC, abstractmethod
from typing import Any, Union, Generic, TypeVar

T = TypeVar("T")


class Wrapper(ABC, Generic[T]):
    """
    Abstract base class for a wrapper. All input/output variables are wrapped 
    in a wrapper so that they can be passed to other scopes as a reference 
    type and so that lexical closures of the input/output data can be passed 
    to the code-execution scope.

    Classes that inherit from `Wrapper` should imitate the behavior of the 
    object they represent (of type `T`). This is done by overloading built-in 
    operators/functions and automatically redirecting everything else  with 
    `__getattr__` and `__setattr__`. Exceptions to this behavior are in the 
    documentation. 
    
    In addition, all wrappers must inherit/implement this class so that when 
    an operation is performed between two or more wrapped objects, they can 
    recognize one another as being Wrapper instances and act accordingly. This 
    pattern can be seen in the operator overloads of the 
    `collections.UserString`, `collections.UserList`, etc. classes.

    Attributes:
        T: The type of the data being wrapped.

    """

    @abstractmethod
    def to(self, new_data: Union[T, Any]) -> None:
        """
        Effectively replaces the `=` operator for the wrapper's data.
        
        Updates the data of the wrapper interface to the specified value. Try 
        to avoid re-assigning an input/output variable, especially to a 
        reference type, as this can lead to unexpected behavior. Instead, try 
        to use a new variable, as it is unlikely that one absolutely needs to 
        set an output variable to point to a reference type.

        Args:
            new_data (Union[T, Any]): The new data value to set.
        """
        pass

    @abstractmethod
    def resolve(self) -> T:
        """
        Returns:
            T: The up-to-date data value of the wrapper.
        """
        pass
