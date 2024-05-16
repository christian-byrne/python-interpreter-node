import torch
from typing import Optional, List, Union
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

try:
    from .wrapper_class import TensorWrapper
except ImportError:
    import sys

    sys.path.append("..")
    from wrapper_class import TensorWrapper


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

    def splice_return_statments(self, code_lines: List[str]):
        returns = [line for line in code_lines if line.strip().startswith("return")]
        non_returns = [
            line for line in code_lines if not line.strip().startswith("return")
        ]
        return non_returns, returns

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

        code_lines, return_statements = self.splice_return_statments(
            python_code.split("\n")
        )
        return_variables = [statement.split()[1] for statement in return_statements]
        # TODO: stateful dummy return instances. capture additional return values and append to outputs

        code = "\n".join(code_lines)
        code = compile(code, "<string>", "exec")

        # Look at the optimization: https://github.com/python/cpython/blob/3.12/Lib/timeit.py
        try:
            f = StringIO()
            err = StringIO()
            with redirect_stdout(f), redirect_stderr(err):
                try:
                    exec(
                        code,
                        {
                            "image1": self.image1,
                            "image2": self.image2,
                            "mask1": self.mask1,
                            "mask2": self.mask2,
                            "number1": self.number1,
                            "number2": self.number2,
                            "text1": self.text1,
                            "text2": self.text2,
                        },
                    )
                except RuntimeError as e:
                    print(e)
                except SyntaxError as e:
                    # TODO: Linting hint
                    print(e)
                except TypeError as e:
                    # trying to reference the variable for an input variable but the input was not piped
                    # TODO: tensor wrapper ignore, operator overloading issue
                    print(e)
                except ImportError as e:
                    # TODO: handle import space/python version
                    print(e)
                except (AttributeError, NameError, ValueError) as e:
                    # TODO: change namespace/context, fuzzy match variable mismatch,
                    #   hint: dont change names of input variables from how they appear in the UI
                    print(e)

        except IOError as e:
            # globals
            # Try changing newline char, try changing encoding, try tempfile, try singleton, try changing file mode
            print(e)
        except Exception as e:
            print(e)

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
            "ui": {
                "text": (
                    f"{f.getvalue()}\n{err.getvalue()}"
                    if give_full_error_stack
                    else f.getvalue()
                )
            },
            "result": result,
        }
