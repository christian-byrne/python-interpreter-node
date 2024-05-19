
from .python_interpreter_node import PythonInterpreter 
        

NODE_CLASS_MAPPINGS = {
    "Exec Python Code Script": PythonInterpreter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Exec Python Code Script": "Python Interpreter"
}

WEB_DIRECTORY = "./web"