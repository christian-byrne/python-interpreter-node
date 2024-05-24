import torch
from contextlib import redirect_stdout, redirect_stderr
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from .wrappers.wrapper_abc import Wrapper
from .wrappers.wrapper_factory import WrapperFactory
from .streams.stream_manager import StandardStreamManager

from typing import Optional, List, Union, Any, Dict


class PythonInterpreter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_code": ("STRING",{
                    "default": "",
                }),
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
        raw_code: str = "",
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
        self.image1 = WrapperFactory(image1)
        self.image2 = WrapperFactory(image2)
        self.mask1 = WrapperFactory(mask1)
        self.mask2 = WrapperFactory(mask2)
        self.number1 = WrapperFactory(number1)
        self.number2 = WrapperFactory(number2)
        self.text1 = WrapperFactory(text1)
        self.text2 = WrapperFactory(text2)
        self.list1 = WrapperFactory(list1)
        self.list2 = WrapperFactory(list2)
        self.dict1 = WrapperFactory(dict1)
        self.dict2 = WrapperFactory(dict2)

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
                "list2",
                "dict1",
                "dict2",
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
