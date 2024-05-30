import torch
from contextlib import redirect_stdout, redirect_stderr
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrappers.wrapper_abc import Wrapper
from .wrappers.wrapper_factory import WrapperFactory
from .streams.stream_manager import StandardStreamManager

from typing import Optional, List, Union, Any, Dict, Set


class PythonInterpreter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_code": (
                    "STRING",
                    {
                        "default": "",
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
                "list1": ("*", {}),
                "dict1": ("*", {}),
                "any1": ("*", {}),
                "any2": ("*", {}),
                "any3": ("*", {}),
                "any4": ("*", {}),
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
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
        "*",
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
        "dict1",
        "any1",
        "any2",
        "any3",
        "any4",
    )
    CATEGORY = "x"

    def run(
        self,
        raw_code: str = "",
        image1: Optional[torch.Tensor] = torch.rand([1, 32, 32, 3]),
        image2: Optional[torch.Tensor] = torch.rand([1, 32, 32, 3]),
        mask1: Optional[torch.Tensor] = torch.rand([1, 32, 32]),
        mask2: Optional[torch.Tensor] = torch.rand([1, 32, 32]),
        number1: Optional[float] = 0.0,
        number2: Optional[int] = 0,
        text1: Optional[str] = "hello",
        text2: Optional[str] = "world",
        list1: Optional[List[Any]] = [1],
        dict1: Optional[Dict[str, Any]] = {"key": 1},
        any1: Optional[Any] = torch.rand([1, 32, 32, 3]),
        any2: Optional[Any] = torch.rand([1, 32, 32, 3]),
        any3: Optional[Any] = torch.rand([1, 32, 32, 3]),
        any4: Optional[Any] = torch.rand([1, 32, 32, 3]),
        verbose: bool = True,
        output_text: str = "",
        unique_id=None,
        extra_pnginfo=None,
    ) -> Dict[str, Any]:
        self.image1 = WrapperFactory.create_wrapper(image1)
        self.image2 = WrapperFactory.create_wrapper(image2)
        self.mask1 = WrapperFactory.create_wrapper(mask1)
        self.mask2 = WrapperFactory.create_wrapper(mask2)
        self.number1 = WrapperFactory.create_wrapper(number1)
        self.number2 = WrapperFactory.create_wrapper(number2)
        self.text1 = WrapperFactory.create_wrapper(text1)
        self.text2 = WrapperFactory.create_wrapper(text2)
        self.list1 = WrapperFactory.create_wrapper(list1)
        self.dict1 = WrapperFactory.create_wrapper(dict1)
        self.any1 = WrapperFactory.create_wrapper(any1)
        self.any2 = WrapperFactory.create_wrapper(any2)
        self.any3 = WrapperFactory.create_wrapper(any3)
        self.any4 = WrapperFactory.create_wrapper(any4)

        self.shared_ref_dict = self.__map_ref_dict(
            [
                "image1",
                "image2",
                "mask1",
                "mask2",
                "number1",
                "number2",
                "text1",
                "text2",
                "list1",
                "dict1",
                "any1",
                "any2",
                "any3",
                "any4",
            ]
        )
        self.out_streams = StandardStreamManager(verbose)
        self.__exec_code(raw_code)
        result = self.close_scope(self.shared_ref_dict)
        return {
            "ui": {"text": str(self.out_streams)},
            "result": result,
        }

    def close_scope(self, ref_dict: Dict[str, Wrapper]) -> List[Any]:
        ret = []
        for value in ref_dict.values():
            if isinstance(value, Wrapper):
                ret.append(value.resolve())
        return ret

    def __exec_code(self, code_raw_text: str):
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

    def __map_ref_dict(self, attributes: List[Any]) -> Dict[str, Wrapper]:
        ref_dict = {attr: getattr(self, attr) for attr in attributes}
        return ref_dict
