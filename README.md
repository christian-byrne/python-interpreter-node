# Python Interpreter ComfyUI Node 🐍

![demo video](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/demos/videos/demo.gif?raw=true)

> [!TIP]
>  To install via manager, you must first open the ComfyUI Manager settings and set the `channel` setting to `dev`:
>
>
>
> <details>
>
> <summary> &nbsp; See Picture of Specified Setting </summary>
> 
> ![channel setting in comfyui manager](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/comfyui-manager-setting.png?raw=true)
>
> </details>
>

## Description

- Write Python code that executes when the workflow is queued
- The stdout/err (e.g., prints, error tracebacks) are displayed in the node. 
- The input values can be accessed by their UI name. 
- The output values are the same as the input values, changes made to input values in the code are reflected in the output values.

## Requirements

- python 3.10+

## Installation

1. `cd` into `ComfyUI/custom_nodes` directory
2. `git clone` this repository

To install via ComfyUI Manager, set the `channels` setting to `dev` and search for `Python Interpreter` in the manager.

## Usage

- The variables in the UI (e.g., `image1`, `number1`, `text1`, etc.) can be accessed directly in the code by the same name
    ```python
    print(image1.shape)
    print(number1 * random.randint(0, 99))
    ```
- The output values share the same names as the input values. Changes you make to these variables will be reflected in the output values.
- The code will work as expected in almost all cases except for i. re-assignment and ii. passing the variables as arguments to external functions.
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
- Refer to the [Images, Latents, and Masks section of comfydocs.org](https://www.comfydocs.org/essentials/custom_node_images_and_masks) for info regarding types.
- Try to avoid re-assigning the input/output variables to objects of a different type. You may lose access to some instance methods. If it must be done (e.g., to get an ouput of a novel type), just do it at the end of the code, and use your own variables in the meantime.

## Examples

#### Get Complementary Colors from Image -> Interpolate into a Prompt

>
>
> <details>
> <summary> &nbsp; Expand Image </summary>
>
> 
> ![demo picture - complementary color palette](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/demos/pictures/new-example-complementary-colors.png?raw=true)
>
> </details>

#### Paste Input Text on Image

>
>
> <details>
> <summary> &nbsp; Expand Image </summary>
>
> 
> ![demo picture = caption composite](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/demos/pictures/new-example-caption-draw.png?raw=true)
>
> </details>

#### Snippets

- [Automatically get color palette and complements from image](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/code-snippets-from-demos/get_complementary_colors.py)
- [Most recent image in folder](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/code-snippets-from-demos/most_recent_image_in_folder.py)
- [Paste text on image](https://github.com/christian-byrne/python-interpreter-node/blob/demo-files/wiki/code-snippets-from-demos/paste_text_caption.py)
- ...[More](https://github.com/christian-byrne/python-interpreter-node/tree/demo-files/wiki/code-snippets-from-demos)


----

*Disclaimer: Do not put this on a server that is accessible to the public. This node can run any Python code provided by a user, including malicious code.*