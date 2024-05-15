import torch
from typing import Optional, List, Union
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import numpy
from PIL import Image


class PythonInterpreter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "python_code": (
                    "STRING",
                    {
                        "default": "# Write your code here.\n# Use image1.tensor to get the raw tensor.\n# You can't re-assign the input variables.\n# Use in-place operators (e.g., -=, +=, *=, **=, //=, /=)\n\nprint(f'image1 shape: {image1.shape}')\nprint(f'image2 shape: {image2.shape}')\nprint(f'mask1 shape: {mask1.shape}')\n\nif image1 != mask1:\n\tprint('image1 and mask1 are not equal')\n\timage1 = image1 - mask1",
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
                        "default": "xd",
                    },
                ),
                "text2": (
                    "STRING",
                    {
                        "default": "xd",
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


class TensorWrapper:
    def __init__(self, tensor):
        if not isinstance(tensor, torch.Tensor):
            if isinstance(tensor, numpy.ndarray):
                self.tensor = torch.from_numpy(tensor)
            if isinstance(tensor, Image.Image):
                self.tensor = torch.tensor(numpy.array(tensor))
            else:
                self.tensor = None
        else:
            self.tensor = tensor

        self.null_msg = (
            "No image passed to an input with the same name as this variable"
        )
        if self.tensor is not None:
            self.shape = tensor.shape
            self.dim = tensor.dim()
        else:
            self.shape, self.dim = self.null_msg, self.null_msg

    def subtract(self, other):
        """
        1 - A: invert mask
        RGB/RGBA - RGB/RGBA: subtract pixel values (difference image)
        RGBA - A: minimum operation on alpha channels

        RGBA/A - number: decrease opacity
        RGBA/RGB - str: remove text from image
        RGB - number: decrease intensity
        """
        if other == "tensor":
            if other.tensor.dim() == 3 and self.is_tensor():
                return self.subtract_mask_from_img(self.tensor, other.tensor)

    def __sub__(self, other):
        return TensorWrapper(self.subtract(other))

    def __isub__(self, other):
        self.tensor = self.subtract(other)

    def subtract_mask_from_img(self, img, mask):
        # RGBA - A
        if img.shape[3] == 4:
            subtracted_alphas = torch.min(img[0][:, :, 3], mask[0])
            return torch.cat(
                (
                    img[0][:, :, :3],
                    subtracted_alphas.unsqueeze(2),
                ),
                dim=2,
            ).unsqueeze(0)
        # RGB - A
        else:
            return torch.cat((img[0][:, :, :3], mask[0].unsqueeze(2)), dim=2).unsqueeze(
                0
            )

    def add(self, other):
        """
        RGB/RGBA + RGB/RGBA: composite

        A + A: max operation on alpha channels
        RGB + A: add alpha channel to RGB
        RGBA + A: max on alpha channels
        RGB/RGBA + number: increase intensity
        str + RGB/RGBA/A or RGB/RGBA/A + str: add text to image
        str which has been multiplied (e.g., "text text text text") + RGB/RGBA/A: add text to image and increase text's size by number of repetitions
        """
        if self == "tensor" and other == "tensor":
            channel_sum = self.shape[3] + other.shape[3]
            if channel_sum >= 6:
                return self.add_img_and_img(self.tensor, other.tensor)
            elif channel_sum > 2:
                return self.add_img_and_mask(self.tensor, other.tensor)
            else:
                return self.add_mask_and_mask(self.tensor, other.tensor)

    def __add__(self, other):
        return TensorWrapper(self.add(other))

    def __iadd__(self, other):
        self.tensor = self.add(other)

    def add_img_and_mask(self, img, mask):
        # RGB/RGBA + A
        return torch.cat(
            (
                img[0][:, :, :3],
                mask[0].unsqueeze(2),
            ),
            dim=2,
        ).unsqueeze(0)

    def add_mask_and_mask(self, mask1, mask2):
        # A + A
        return torch.max(mask1[0], mask2[0]).unsqueeze(0)

    def add_img_and_img(self, img1: torch.Tensor, img2: torch.Tensor):
        # RGB + RGBA or RGBA + RGB
        if img1.shape[3] != img2.shape[3] and img1.shape[3] == 3:
            img1[:, :, :, 3] = 1
            print(img1.shape, img2.shape)
            return torch.where(
                img2[:, :, :, 3] == 0,
                img2,
                img1,
            )
        if img2.shape[3] != img1.shape[3] and img2.shape[3] == 3:
            img2[:, :, :, 3] = 1
            print(img1.shape, img2.shape)
            return torch.where(
                img1[:, :, :, 3] == 0,
                img1,
                img2,
            )
        print(img1.shape, img2.shape)
        img1 = img1.squeeze(0)
        img2 = img2.squeeze(0)
        alpha1 = img1[:, :, 3].unsqueeze(2)
        print(alpha1.shape, img1.shape, img2.shape)
        ret = img1[:, :, :3] * alpha1 + img2[:, :, :3] * (1 - alpha1)
        print(ret.shape)
        return ret.unsqueeze(0)

    def size(self):
        if self.tensor is None:
            return None
        return self.tensor.size()

    def is_tensor(self):
        return isinstance(self.tensor, torch.Tensor)

    def resolve(self):
        # TODO:
        return self.tensor

    def __repr__(self):
        return f"ImageTensorWrapper({self.shape})"

    def __str__(self):
        if self.tensor is not None:
            return f"ImageTensorWrapper(shape: {self.shape}, dim: {self.dim}, dtype: {self.tensor.dtype}, device: {self.tensor.device})"
        return "NoneType"

    # def __floor__(self):
    #     # TODO
    #     return self.tensor

    # def __pos__(self):
    #     # Unary positive: +tensor
    #     # FROM A: convert to image
    #     pass

    # def __neg__(self):
    #     # Unary negative: -tensor
    #     # FROM A: convert to mask
    #     pass

    # def __abs__(self):
    #     # absolute value: abs(tensor)
    #     # ....
    #     pass

    # def __invert__(self):
    #     # bitwise NOT: ~tensor
    #     # FROM A: invert mask
    #     # FROM RGB: invert image colors (1 - normalized rgb values)
    #     # FROM RGBA: invert alpha channel
    #     pass

    # def __round__(self):
    #     # round to nearest: round(tensor)
    #     # FROM RGB/RGBA: infer alpha from rgb values
    #     pass

    def __eq__(self, other: Union[torch.Tensor, str]):
        # equal: tensor == other
        # RGB/RGBA/A == "tensor"
        if isinstance(other, str) and other == "tensor":
            return self.is_tensor()
        # FROM RGB/RGBA/A: compare sizes for equality
        # RGB/RGBA/A == RGB/RGBA/A: compare pixel values for equality
        if isinstance(other, torch.Tensor):
            if torch.equal(self.tensor, other):
                return True
        return False

    def __ne__(self, other):
        # not equal: tensor != other
        # FROM RGB/RGBA/A: compare sizes for inequality
        return not self.__eq__(other)

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

    # def __mul__(self, other):
    #     # multiplication: tensor * other
    #     # A * A: normal matrix multiplication
    #     # RGB/RGBA * A: one-zero matrix addition
    #     # RGB/RGBA * number: increase size of image by number
    #     pass

    # def __truediv__(self, other):
    #     # division: tensor / other
    #     # RGB/RGBA/A / number: decrease size of image by number
    #     # RGB/RGBA/A / (number, number): resize to size of tuple
    #     # RGB/RGBA/A / RGB/RGBA/A: resize to size of 2nd image, changing aspect ratio if necessary
    #     pass

    # def __floordiv__(self, other):
    #     # floor division: tensor // other
    #     # RGB/RGBA // number: decrease size of image by number, rounding down
    #     # RGB/RGBA // (number, number): resize to size of tuple, maintaing aspect ratio
    #     # RGB/RGBA/A // RGB/RGBA/A: resize to size of 2nd image, maintaing aspect ratio via crop or padding
    #     pass

    # def __pow__(self, other):
    #     # tensor ** other
    #     # FROM A to A: matrix power
    #     # FROM RGB/RGBA to RGB/RGBA: apply gamma correction
    #     # RGB/RGBA ** number: add self to batch with number copies
    #     pass

    # def __or__(self, other):
    #     # bitwise OR: tensor | other
    #     # pad lower by other pixels
    #     pass

    # def __xor__(self, other):
    #     # bitwise XOR: tensor ^ other
    #     # pad upper by other pixels
    #     pass

    # def __lshift__(self, other):
    #     # bitwise left shift: tensor << other
    #     # pad left by other pixels
    #     pass

    # def __rshift__(self, other):
    #     # bitwise right shift: tensor >> other
    #     # pad right by other pixels
    #     pass

    # def __getitem__(self, key):
    #     # tensor[key]
    #     # RGBA/RGB/A[key]: get key-index item in batch
    #     pass

    # def __setitem__(self, key, value):
    #     # tensor[key] = value
    #     # RGBA/RGB/A[key] = RGBA/RGB/A: set key-index color channel to match value of other
    #     # RGBA/RGB/A[1] = number: set width to number
    #     # RGBA/RGB/A[2] = number: set height to number
    #     pass

    # def __delitem__(self, key):
    #     # del tensor[key]
    #     # del RGBA/RGB/A[key]: remove key-index item from batch
    #     pass

    # def __len__(self):
    #     # len(tensor)
    #     # len(RGBA/RGB/A): number of items in batch
    #     pass

    # def __iter__(self):
    #     # iter(tensor)
    #     # iter(RGBA/RGB/A): iterate over items in batch
    #     pass

    # def __contains__(self, item):
    #     # item in tensor
    #     # CHW in BCHW: check if item is in batch
    #     # (number, number, number) in RGBA/RGB/A: check if rgb value is a term in tensor
    #     # number in RGBA/RGB/A: check if number is either height or width
    #     # (number, number) in RGBA/RGB/A: check if a tensor with those dimensions exists in the batch
    #     # 0 in RGBA/RGB/A: check if there is a hole in the image
    #     # item in RGBA/RGB/A: check if item is in batch
    #     pass

    # def __call__(self, *args, **kwargs):
    #     # tensor(*args, **kwargs)
    #     # RGBA/RGB/A(*args, **kwargs): apply function to each item in batch
    #     pass
