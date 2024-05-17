import torch
from typing import Optional, List, Union
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

try:
    from .image_tensor_wrapper import TensorWrapper
except ImportError:
    import sys

    sys.path.append("..")
    from image_tensor_wrapper import TensorWrapper


class PythonInterpreter:
    CODE_PLACEHOLDER = "\n".join(
        [
            "# Write your code here.",
            "# Use image1.tensor to get the raw tensor",
            "# Don't re-assign input variables using = operator",
            "# \tInstead, use .to() (like, image1.to(image1 * mask1))"
            "# \tOr use in-place operators (e.g., -=, +=, *=, **=, //=, /=)",
            "# \tHowever, you can change the input variables attributes per usual",
        ]
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "python_code": (
                    "STRING",
                    {
                        "default": cls.CODE_PLACEHOLDER,
                        "multiline": True,
                    },
                ),
            },
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "mask1": ("MASK",),
                "mask2": ("MASK",),
                "number1": (
                    "FLOAT",
                    {
                        "default": 0.0,
                    },
                ),
                "number2": (
                    "FLOAT",
                    {
                        "default": 0,
                    },
                ),
                "text1": (
                    "STRING",
                    {
                        "default": "hello world",
                    },
                ),
                "text2": (
                    "STRING",
                    {
                        "default": "hello world",
                    },
                ),
                "give_full_error_stack": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "use_wrapper_class": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "output_text": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = (
        "IMAGE",
        "IMAGE",
        "MASK",
        "MASK",
        "NUMBER",
        "NUMBER",
        "STRING",
        "STRING",
    )

    def run(
        self,
        python_code: str,
        image1: Optional[torch.Tensor] = None,
        image2: Optional[torch.Tensor] = None,
        mask1: Optional[torch.Tensor] = None,
        mask2: Optional[torch.Tensor] = None,
        number1: Optional[Union[float, int, complex]] = None,
        number2: Optional[Union[float, int, complex]] = None,
        text1: Optional[str] = None,
        text2: Optional[str] = None,
        give_full_error_stack: bool = False,
        use_wrapper_class: bool = False,
        output_text: str = "",
        unique_id=None,
        extra_pnginfo=None,
    ):
        self.image1 = TensorWrapper(image1)
        self.image2 = TensorWrapper(image2)
        self.mask1 = TensorWrapper(mask1)
        self.mask2 = TensorWrapper(mask2)
        self.number1 = number1
        self.number2 = number2
        self.text1 = text1
        self.text2 = text2

        code_lines, return_statements = self.__splice_return_statments(
            python_code.split("\n")
        )
        return_variables = [statement.split()[1] for statement in return_statements]
        # TODO: stateful dummy return instances. capture additional return values and append to outputs

        code = "\n".join(code_lines)
        compiled_code = compile(compiled_code, "<string>", "exec")
        error_messages = []
        shared_ref_dict = {
            "image1": self.image1,
            "image2": self.image2,
            "mask1": self.mask1,
            "mask2": self.mask2,
            "number1": self.number1,
            "number2": self.number2,
            "text1": self.text1,
            "text2": self.text2,
        }
        try_imports = [
            "torch", "numpy", "random", "time", "os", "sys", "math", "re", "json", "csv", "collections", "itertools",
        ]
        try_imports = "\n".join([f"import {lib}" for lib in try_imports])

        # Look at the optimization: https://github.com/python/cpython/blob/3.12/Lib/timeit.py
        try:
            f = StringIO()
            err = StringIO()
            try:
                with redirect_stdout(f), redirect_stderr(err):
                    exec(
                        compiled_code,
                        shared_ref_dict,
                    )
            except RuntimeError as e:
                error_messages.extend([
                    "\nRuntime Error: Check that your code is not causing an infinite loop or that it is not using too much memory.",
                    str(e) + "\n",
                ])
                print(e)
            except SyntaxError as e:
                # TODO: Add linter and Linting hint
                print(e)
            except TypeError as e:
                error_messages.extend([
                    "\nType Error: If you are referencing an input variable, make sure you are actually piping something in to that slot and that the value is of the correct type. If you want to reference an image/mask's tensor, use the tensor attribute (e.g., image1.tensor).",
                    str(e) + "\n",
                ])
                print(e)
            except ImportError as e:
                compiled_code = compile(f"{try_imports}\n{code}", "<string>", "exec")
                try:
                    with redirect_stdout(f), redirect_stderr(err):
                        exec(
                            compiled_code,
                            shared_ref_dict,
                        )
                except ImportError as e:
                    error_messages.extend([
                        "\nImport Error: Don't forget to import any libraries used in your code. Use pip install to install any missing libraries.",
                        str(e) + "\n",
                    ])
                    print(e)
            except (AttributeError, NameError, ValueError) as e:
                error_messages.extend([
                    "\nName Error: Check that the variable names used in your code match the input variables. Don't try to change the names of the input variables from how they appear in the UI.",
                    str(e) + "\n",
                ])
                # TODO: fuzzy match variable mismatch,
                print(e)

        except IOError as e:
            # Can also try tempfile or changing filemode
            compiled_code = compile(code.replace("\n", "\r\n"), "<string>", "exec")
            with redirect_stdout(f), redirect_stderr(err):
                exec(
                    compiled_code,
                    shared_ref_dict,
                )

            print(e)
        except Exception as e:
            error_messages.extend([
                "\nUnknown Error: Something went wrong. Check the error message for more details.",
                str(e) + "\n",
            ])
            print(e)

        stdout_display = f"{f.getvalue()}\n{err.getvalue()}\n{'\n'.join(error_messages)}"
        result = (
            self.image1.resolve(),
            self.image2.resolve(),
            self.mask1.resolve(),
            self.mask2.resolve(),
            self.number1,
            self.number2,
            self.text1,
            self.text2,
        )
        return {
            "ui": {"text": stdout_display},
            "result": result,
        }

    def __splice_return_statments(self, code_lines: List[str]):
        returns = [line for line in code_lines if line.strip().startswith("return")]
        non_returns = [
            line for line in code_lines if not line.strip().startswith("return")
        ]
        return non_returns, returns
