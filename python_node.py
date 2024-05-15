import torch
from typing import Optional, List


class ImageTensorWrapper:
    def __init__(self, tensor):
        if not isinstance(tensor, torch.Tensor):
            self = None
            return

        self.tensor = tensor

    def __repr__(self):
        return f"ImageTensorWrapper({self.tensor.shape})"

    def __floor__(self):
        # TODO
        return self.tensor

    def __pos__(self):
        # Unary positive: +tensor
        # FROM A: convert to image
        pass

    def __neg__(self):
        # Unary negative: -tensor
        # FROM A: convert to mask
        pass

    def __abs__(self):
        # absolute value: abs(tensor)
        # ....
        pass

    def __invert__(self):
        # bitwise NOT: ~tensor
        # FROM A: invert mask
        # FROM RGB: invert image colors (1 - normalized rgb values)
        # FROM RGBA: invert alpha channel
        pass

    def __round__(self):
        # round to nearest: round(tensor)
        # FROM RGB/RGBA: infer alpha from rgb values
        pass

    def __eq__(self, other):
        # equal: tensor == other
        # FROM RGB/RGBA/A: compare sizes for equality
        pass

    def __ne__(self, other):
        # not equal: tensor != other
        # FROM RGB/RGBA/A: compare sizes for inequality
        pass

    def __lt__(self, other):
        # less than: tensor < other
        # FROM RGB/RGBA/A: compare sizes for less than
        pass

    def __le__(self, other):
        # less or equal: tensor <= other
        # FROM RGB/RGBA/A: compare sizes for less or equal
        pass

    def __gt__(self, other):
        # greater than: tensor > other
        # FROM RGB/RGBA/A: compare sizes for greater than
        pass

    def __ge__(self, other):
        # greater or equal: tensor >= other
        # FROM RGB/RGBA/A: compare sizes for greater or equal
        pass

    def __add__(self, other):
        # addition: tensor + other
        # FROM RGB to A or A to RGB: combine to RGBA
        # FROM A to RGBA or RGBA to A: one-zero matrix elementwise multiplication (only keep if both 1)
        # FROM A to A: one-zero matrix elementwise multiplication
        # FROM RGB/RGBA to RGB/RGBA: picture compositing, 2nd image as base, 1st image as overlay
        # FROM str to RGB/RGBA/A or RGB/RGBA/A to str: add text to image
        # FROM str which has been multiplied (e.g., "text text text text") to RGB/RGBA/A: add text to image and increase text's size by number of repetitions
        pass

    def __sub__(self, other):
        # subtraction: tensor - other
        # 1 - A: invert mask
        # RGB/RGBA - RGB/RGBA: subtract pixel values (difference image)
        # RGB/RGBA - A: masked crop
        # RGBA/A - number: decrease opacity
        # RGBA/RGB - str: remove text from image
        # RGB - number: decrease intensity
        pass

    def __mul__(self, other):
        # multiplication: tensor * other
        # A * A: normal matrix multiplication
        # RGB/RGBA * A: one-zero matrix addition
        # RGB/RGBA * number: increase size of image by number
        pass

    def __truediv__(self, other):
        # division: tensor / other
        # RGB/RGBA/A / number: decrease size of image by number
        # RGB/RGBA/A / (number, number): resize to size of tuple
        # RGB/RGBA/A / RGB/RGBA/A: resize to size of 2nd image, changing aspect ratio if necessary
        pass

    def __floordiv__(self, other):
        # floor division: tensor // other
        # RGB/RGBA // number: decrease size of image by number, rounding down
        # RGB/RGBA // (number, number): resize to size of tuple, maintaing aspect ratio
        # RGB/RGBA/A // RGB/RGBA/A: resize to size of 2nd image, maintaing aspect ratio via crop or padding
        pass

    def __pow__(self, other):
        # tensor ** other
        # FROM A to A: matrix power
        # FROM RGB/RGBA to RGB/RGBA: apply gamma correction
        # RGB/RGBA ** number: add self to batch with number copies
        pass

    def __or__(self, other):
        # bitwise OR: tensor | other
        # pad lower by other pixels
        pass

    def __xor__(self, other):
        # bitwise XOR: tensor ^ other
        # pad upper by other pixels
        pass

    def __lshift__(self, other):
        # bitwise left shift: tensor << other
        # pad left by other pixels
        pass

    def __rshift__(self, other):
        # bitwise right shift: tensor >> other
        # pad right by other pixels
        pass

    def __str__(self):
        return f"ImageTensorWrapper({self.tensor.shape})"

    def __getitem__(self, key):
        # tensor[key]
        # RGBA/RGB/A[key]: get key-index item in batch
        pass

    def __setitem__(self, key, value):
        # tensor[key] = value
        # RGBA/RGB/A[key] = RGBA/RGB/A: set key-index color channel to match value of other
        # RGBA/RGB/A[1] = number: set width to number
        # RGBA/RGB/A[2] = number: set height to number
        pass

    def __delitem__(self, key):
        # del tensor[key]
        # del RGBA/RGB/A[key]: remove key-index item from batch
        pass

    def __len__(self):
        # len(tensor)
        # len(RGBA/RGB/A): number of items in batch
        pass

    def __iter__(self):
        # iter(tensor)
        # iter(RGBA/RGB/A): iterate over items in batch
        pass

    def __contains__(self, item):
        # item in tensor
        # CHW in BCHW: check if item is in batch
        # (number, number, number) in RGBA/RGB/A: check if rgb value is a term in tensor
        # number in RGBA/RGB/A: check if number is either height or width
        # (number, number) in RGBA/RGB/A: check if a tensor with those dimensions exists in the batch
        # 0 in RGBA/RGB/A: check if there is a hole in the image
        # item in RGBA/RGB/A: check if item is in batch
        pass

    def __call__(self, *args, **kwargs):
        # tensor(*args, **kwargs)
        # RGBA/RGB/A(*args, **kwargs): apply function to each item in batch
        pass


class PythonInterpreter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "python_code": (
                    "STRING",
                    {"default": "# Write your code here", "multiline": True},
                ),
            },
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "mask1": ("MASK",),
                "mask2": ("MASK",),
                "latent": ("LATENT",),
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    def splice_return_statments(self, code_lines: List[str]):
        returns = [line for line in code_lines if line.strip().startswith("return")]
        non_returns = [
            line for line in code_lines if not line.strip().startswith("return")
        ]
        return non_returns, returns

    #   https://github.com/python/cpython/blob/3.12/Lib/timeit.py
    def run(
        self,
        python_code: str,
        image1: Optional[torch.Tensor] = None,
        image2: Optional[torch.Tensor] = None,
        mask1: Optional[torch.Tensor] = None,
        mask2: Optional[torch.Tensor] = None,
        latent: Optional[torch.Tensor] = None,
    ):
        image1 = ImageTensorWrapper(image1)
        image2 = ImageTensorWrapper(image2)
        mask1 = ImageTensorWrapper(mask1)
        mask2 = ImageTensorWrapper(mask2)

        # Define the function
        code_lines = python_code.split("\n")
        code_lines, return_statements = self.splice_return_statments(code_lines)
        code = "\n".join(code_lines)
        code = compile(code, "<string>", "exec")
        try:
            exec(code)
        except Exception as e:
            return str(e)
        return "Success"
