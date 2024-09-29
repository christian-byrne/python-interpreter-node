from rich import print
from server import PromptServer
from aiohttp import web
from pathlib import Path

from .python_interpreter_node import PythonInterpreter 
        

NODE_CLASS_MAPPINGS = {
    "Exec Python Code Script": PythonInterpreter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Exec Python Code Script": "Python Interpreter"
}

WEB_DIRECTORY = "./web"

ACE_PATH = Path(__file__).parent / "lib-ace"
if ACE_PATH.exists():
    PromptServer.instance.app.router.add_routes(
        [web.static("/lib-ace", ACE_PATH.as_posix())]
    )
else:
    print(f"python_interpreter_node: ACE_PATH does not exist: {ACE_PATH}")