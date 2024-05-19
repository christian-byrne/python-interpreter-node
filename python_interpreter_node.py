import torch
from typing import Optional, List, Union
from contextlib import redirect_stdout, redirect_stderr

try:
    from .image_tensor_wrapper import TensorWrapper
    from .stream_wrapper import StandardStreamWrapper
except ImportError:
    import sys

    sys.path.append("..")
    from image_tensor_wrapper import TensorWrapper
    from stream_wrapper import StandardStreamWrapper


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
                "verbose": (
                    "BOOLEAN",
                    {
                        "default": True,
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
        verbose: bool = True,
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
        # TODO: return instances. capture additional return values and append to outputs

        code = "\n".join(code_lines)
        self.shared_ref_dict = {
            "image1": self.image1,
            "image2": self.image2,
            "mask1": self.mask1,
            "mask2": self.mask2,
            "number1": self.number1,
            "number2": self.number2,
            "text1": self.text1,
            "text2": self.text2,
        }
        self.out_streams = StandardStreamWrapper(verbose)
        self.__exec_code(code)
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
            "ui": {"text": str(self.out_streams)},
            "result": result,
        }

    def __exec_code(self, code_raw_text: str):
        # Look at the optimization: https://github.com/python/cpython/blob/3.12/Lib/timeit.py
        compiled_code = compile(code_raw_text, "<string>", "exec")
        try:
            with redirect_stdout(self.out_streams.get_out_io()), redirect_stderr(
                self.out_streams.get_err_io()
            ):
                exec(
                    compiled_code,
                    self.shared_ref_dict,
                )
        except Exception as e:
            self.out_streams.write_err(e)

    def __splice_return_statments(self, code_lines: List[str]):
        returns = [line for line in code_lines if line.strip().startswith("return")]
        non_returns = [
            line for line in code_lines if not line.strip().startswith("return")
        ]
        return non_returns, returns