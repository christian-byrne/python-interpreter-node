import cv2
hex_color = text1 # text1 is the first text input in the node

def hex_to_rgb(hex_):
    hex_ = hex_.lstrip("#")
    return tuple(int(hex_[i:i+2], 16) for i in (0, 2, 4))

# We can even add type checks to prevent frustration or inconsistencies with other node outputs
if not isinstance(hex_color, str):
    hex = str(hex_color)

red, green, blue = hex_to_rgb(hex_color)

# Output integer values representing r, g, b
number1.to(int(red))
number2.to(int(green))
number3.to(int(blue))