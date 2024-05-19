from io import StringIO
from collections import deque
import traceback


class StandardStreamWrapper:
    def __init__(self, verbose: bool):
        self.full_traceback = verbose
        self.also_print_system = verbose

        self.hint_messages = deque()
        self.err_io = StringIO()
        self.out_io = StringIO()

        self.hints = {
            "RuntimeError": "Check that your code is not causing an infinite loop or that it is not using too much memory.",
            "TypeError": "If you are referencing an input variable, make sure you are actually piping something in to that slot and that the value is of the correct type. If you want to reference an image/mask's tensor, use the tensor attribute (e.g., image1.tensor).",
            "ImportError": "Use pip install to install any missing libraries. Ensure you install with same version of python or same env you use to run ComfyUI.",
            "NameError": "Check that the variable names used in your code match the input variables and that you included all necessary imports. Don't try to change the names of the input variables from how they appear in the UI.",
        }

    def get_err_io(self) -> StringIO:
        return self.err_io

    def get_out_io(self) -> StringIO:
        return self.out_io

    def write_err(self, err: Exception) -> None:
        if self.also_print_system:
            traceback.print_exc()

        exception_name = err.__class__.__name__

        if exception_name in self.hints:
            self.hint_messages.append(f"{exception_name}: {self.hints[exception_name]}")
        if self.full_traceback:
            self.hint_messages.append(traceback.format_exc())
        else:
            self.hint_messages.append(str(err))

    def __str__(self) -> str:
        err_text = self.err_io.getvalue().strip()
        out_text = self.out_io.getvalue().strip()
        hint_text = "\n".join(self.hint_messages)
        out = ""
        if out_text:
            out += f"Output:\n{out_text}\n"
        if err_text:
            out += f"\nError:\n{err_text}\n"
        if hint_text:
            out += f"\nHint:\n{hint_text}\n"
        return out
