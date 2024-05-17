import torch
import numpy
from PIL import Image
from typing import Union


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
