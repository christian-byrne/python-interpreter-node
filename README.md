# Python Interpreter ComfyUI Node

**Code -> Stdout/Err**

![alt text](wiki/pictures/demos/example1-in_out.png)

**Reassigning/Modifying Inputs and getting from Outputs**

![alt text](wiki/pictures/demos/example1-with_images.png)

**Complex Example - Writing a Text Caption Function**

![alt text](wiki/pictures/demos/example1-caption_composite.png)


### Description

- Allows you to write Python code in the textarea of the node which executes when the workflow is queued
- The stdout/stderr (e.g., prints, error tracebacks) are displayed in the node. 
- The input values can be accessed by their UI name. 
- The output values can be set by assigning to their UI-names.

Features Implemented so Far:
- [x] Code execution (5/16)
- [x] Input value modification and output (5/17)
- [x] Stdout/err display (5/19)
- [x] Output value assignment/pipe (5/19)
- [ ] Code editor plugin
- [ ] Dynamic inputs/outputs
- [ ] Testing and Docs



## Reason to Use

- Anything that can be done with Python code
- Embedding little scripts into your saved workflows
- Quickly make a node that can do a specialized task
- Converting types
- Doing math with input values
- Debugging
- Testing custom nodes faster.


## Usage

- The variables in the UI (e.g., `image1`, `number1`, `text1`, etc.) can be accessed directly in the code by the same name
    ```python
    print(image1.shape)
    print(number1 * random.randint(0, 99))
    ```
- The output values share the same names as the input values. Changes you make to these variables will be reflected in the output values.
- The code will work as expected in almost all cases except for 1. re-assignment and 2. passing the variables as arguments to functions.
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
  2. To pass the variables as arguments to functions, just pass the `.data` attribute of the variable instead
      ```python
      # Instead of pil_img = ToPILImage()(image1):
      pil_img = ToPILImage()(image1.data)

      # Not necessary for built-in functions
      print(image1)
      print(len(text1))
      ```
