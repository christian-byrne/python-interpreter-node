# Python Interpreter ComfyUI Node 🐍

![demo video](wiki/demos/videos/demo.gif)

## Description

- Write Python code in a node that executes when the workflow is queued
- The stdout/stderr (e.g., prints, error tracebacks) are displayed in the node. 
- The input values can be accessed by their UI name. 
- The output values are the same as the input values, changes made to input values in the code are reflected in the output values.

## Requirements

- python 3.10+

## Installation

1. `cd` int `ComfyUI/custom_nodes` directory
2. `git clone` this repository

## Reason to Use

- Embedding scripts into workflows
- Specialized tasks
- Converting types
- Doing math
- Debugging
- Testing custom nodes
- Even if you can't code, you can ask ChatGPT to write a python snippet


## Usage

- The variables in the UI (e.g., `image1`, `number1`, `text1`, etc.) can be accessed directly in the code by the same name
    ```python
    print(image1.shape)
    print(number1 * random.randint(0, 99))
    ```
- The output values share the same names as the input values. Changes you make to these variables will be reflected in the output values.
- The code will work as expected in almost all cases except for i. re-assignment and ii. passing the variables as arguments to functions.
  1.  To re-assign a variable, you must use its `to()` method, regardless of the variable's type
      ```python
      # Instead of number1 = float(number1):
      number1.to(float(number1))

      # Instead of image1 = 0.5 * (image1 + image2):
      image1.to(0.5 * (image1 + image2))

      # Instead of mask1 = 1 - mask1:
      mask1.to(1 - mask1)

      # Instead of text1 = text1.replace("bad", ""):
      text1.to(text1.replace("bad", ""))

      # In-place operators (+=, ++, /=, etc.) will work normally
      number1++
      text1 += " is good"
      ```
  2. To pass the variables as arguments to functions, just pass the `.data` attribute of the variable instead (regardless of the variable's type)
      ```python
      # Instead of pil_img = ToPILImage()(image1):
      pil_img = ToPILImage()(image1.data)

      # Instead of random.sample[number1, number2]:
      random.sample([number1.data, number2.data])

      # Not necessary for built-in functions
      print(image1) # works
      print(len(text1)) # works
      ```
- To understand the type and shape of the input images/masks, please refer to the [Images, Latents, and Masks section of comfydocs.org](https://www.comfydocs.org/essentials/custom_node_images_and_masks).


## Examples

![demo picture - complementary color palette](wiki/demos/pictures/new-example-complementary-colors.png)

![demo picture = caption composite](wiki/demos/pictures/new-example-caption-draw.png)


- [Automatically get color palette and complements from image](wiki/code-snippets-from-demos/get_complementary_colors.py)
- [Most recent image in folder](wiki/code-snippets-from-demos//most_recent_image_in_folder.py)
- [Paste text on image](wiki/code-snippets-from-demos/paste_text_caption.py)
- ...[More snippets in wiki](wiki/code-snippets-from-demos)


----

*Disclaimer: Do not put this on a server that is accessible to the public. This node can run any Python code provided by a user, including malicious code.*