# TODO


- CREATE SINGULAR FACTORY FUNCTION THAT ITERATES OVER ALL POSSIBLE TYPES. THEN IN EACH WRAPPERS `__new__` METHOD, THAT FACTORY FUNCTION WILL BE CALLED TO GET THE RIGHT TYPE OF WRAPPER. THIS WILL ALLOW FOR EASY ADDITION OF NEW WRAPPERS AND WILL MAKE THE CODE MORE READABLE.
- Test the refactoring of the wrapper abc file and filename
- The current `__init__` methods should be changed so their logic is moved to their `__new__` methods and so that if the type passed is wrong, it instead creates an instance of a different wrapper then returns that in the init call. Requires testing that the right type of instance is returned and that all expected behaviour is captured by the delegation. Example:
  ```python
  def __new__(cls, value):
      if isinstance(value, cls._type):
          return super().__new__(cls)
      elif isinstance(value, torch.Tensor):
          return TensorWrapper(value)
      elif isinstance(value, np.ndarray):
          return NumpyWrapper(value)
      else:
          raise TypeError(f"Cannot create {cls.__name__} from {type(value).__name__}")

  def __init__(self, value):
      self._value = value
  ```

  