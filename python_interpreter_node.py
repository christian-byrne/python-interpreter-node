import torch
from typing import Optional, List, Union, Any
from contextlib import redirect_stdout, redirect_stderr
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrappers.string_wrapper import StringWrapper
from .wrappers.number_wrapper import NumberWrapper
from .wrappers.image_tensor_wrapper import TensorWrapper
from .wrappers.list_wrapper import ListWrapper
from .wrappers.dict_wrapper import DictWrapper
from .streams.stream_manager import StandardStreamManager


class PythonInterpreter:
    # CODE_PLACEHOLDER = "\n".join(
    #     [
    #         "# Docs: https://github.com/christian-byrne/python-interpreter-node",
    #         "",
    #         "# Use .to() to re-assign the value of input/output variables",
    #         "list1.to([1, 2, 3, 4])",
    #         "number1.to(3.14)",
    #         "",
    #         "# If passing inputs/outputs as args to non-builtins, use .data",
    #         "from torchvision.transforms import ToPILImage",
    #         "image1.to(image1.squeeze(0).permute(2, 0, 1)) # From BHWC to CHW",
    #         "image1_pil = ToPILImage()(image1.data) # Use .data when passing as arg",
    #         "image1_pil.show()",
    #         "image1.to(image1.permute(1, 2, 0).unsqueeze(0)) # Back to BHWC",
    #         "",
    #         "# In all other cases, code behaves like normal python code",
    #         "# Any variables you define yourself will behave as expected",
    #         "print(image1, image2, mask1, mask2, number1, number2, sep='\\n')",
    #         "print(text1, text2, dict1, dict2, list1, list2, sep='\\n')",
    #     ]
    # )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # "python_code": (
                #     "STRING",
                #     {
                #         "default": cls.CODE_PLACEHOLDER,
                #         "multiline": True,
                #     },
                # ),
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
                    "INT",
                    {
                        "default": 0,
                    },
                ),
                "text1": (
                    "STRING",
                    {
                        "default": "hello",
                    },
                ),
                "text2": (
                    "STRING",
                    {
                        "default": "world",
                    },
                ),
                "list1": (
                    "ANY",
                    {},
                ),
                "list2": (
                    "ANY",
                    {},
                ),
                "dict1": ("ANY", {}),
                "dict2": ("ANY", {}),
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
        "ANY",
        "ANY",
        "ANY",
        "ANY",
    )
    RETURN_NAMES = (
        "image1",
        "image2",
        "mask1",
        "mask2",
        "number1",
        "number2",
        "text1",
        "text2",
        "list1",
        "list2",
        "dict1",
        "dict2",
    )
    CATEGORY = "x"

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
        list1: Optional[Union[List, str, Any]] = None,
        list2: Optional[Union[List, str, Any]] = None,
        dict1: Optional[Union[dict, str, Any]] = None,
        dict2: Optional[Union[dict, str, Any]] = None,
        verbose: bool = True,
        output_text: str = "",
        unique_id=None,
        extra_pnginfo=None,
    ):
        self.image1 = TensorWrapper(image1)
        self.image2 = TensorWrapper(image2)
        self.mask1 = TensorWrapper(mask1)
        self.mask2 = TensorWrapper(mask2)
        self.number1 = NumberWrapper(number1)
        self.number2 = NumberWrapper(number2)
        self.text1 = StringWrapper(text1)
        self.text2 = StringWrapper(text2)
        self.list1 = ListWrapper(list1)
        self.list2 = ListWrapper(list2)
        self.dict1 = DictWrapper(dict1)
        self.dict2 = DictWrapper(dict2)

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
            "list1": self.list1,
            "list2": self.list2,
            "dict1": self.dict1,
            "dict2": self.dict2,
        }
        self.out_streams = StandardStreamManager(verbose)
        self.__exec_code(code)
        result = (
            self.image1.resolve(),
            self.image2.resolve(),
            self.mask1.resolve(),
            self.mask2.resolve(),
            self.number1.resolve(),
            self.number2.resolve(),
            self.text1.resolve(),
            self.text2.resolve(),
            self.list1.resolve(),
            self.list2.resolve(),
            self.dict1.resolve(),
            self.dict2.resolve(),
        )
        return {
            "ui": {"text": str(self.out_streams)},
            "result": result,
        }

    def __exec_code(self, code_raw_text: str):
        # Look at the optimization: https://github.com/python/cpython/blob/3.12/Lib/timeit.py
        compiled_code = compile(code_raw_text, "<string>", "exec")
        try:
            with redirect_stdout(self.out_streams.get_out()), redirect_stderr(
                self.out_streams.get_err()
            ):
                exec(
                    compiled_code,
                    self.shared_ref_dict,
                )
        except Exception as e:
            self.out_streams.write_err(e)

    def __splice_return_statments(self, code_lines: List[str]):
        """Don't remove nested returns"""
        returns = [line for line in code_lines if line.startswith("return")]
        non_returns = [line for line in code_lines if not line.startswith("return")]
        return non_returns, returns
