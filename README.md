# Python Interpreter ComfyUI Node

...Work in Progress (5/17/24). Features Implemented so Far:
- [x] Code execution
- [x] Stdout/err display
- [x] Input value modification and output
- [ ] Output value assignment/pipe (an output value not associated with an input)
- [ ] Code editor plugin
- [ ] Dynamic inputs/outputs
- [ ] Testing and Docs

**Description**:

- Allows you to write Python code in the textarea of the node. When the node is executed, the code is run in a Python interpreter. 

- The stdout (includes print() statements, errors, evals, etc.) is displayed in the node. 

- The input values can be accessed by name in the code. The output values can be set by assigning to them in the code.

![alt text](wiki/pictures/demos/p1-zoom.png)

![alt text](wiki/pictures/demos/p1.png)



**Uses**:

- Debugging
  - Testing custom nodes faster.
- Doing any task that can be accomplished with Python code but you don't have a node for
- Saving the node's state as a part of workflow effectively saves mini scripts as nodes in the workflow
- Using logical operators to change the behavior of the queue workflow dynamically
- Converting types
  - Circumventing issues where different nodes provide values in different types and you need to add conditional conversions or formatting
- Doing math with input values

**Wrapper Class with Operator Overloading**:

![alt text](wiki/pictures/demos/p2.png)

- Wrapper class around tensors with operator overloading for doing common image manipulation tasks.I might remove this aspect

# Future

## Possible Features

- "Convert to Custom Node" button
  - Takes the code and creates a node class that simulates the code's behavior
  - Write the code to a python file in the custom_nodes folder, after doing the neccessary setup tasks
- Interactive Console
  - Save locals binaries per queued execution, then reference them in the console so that it can be used anytime 
- Dynamic Inputs/Outputs
- Code Editor JS library integration
- embedded python favicon
- Add dynamic info into the CODE_PLACEHOLDER
  - python version
  - torch version 

## Plan

- [ ] Finish core features
  - [x] Code execution
    - [ ] Error delegation
  - [ ] Dynamic inputs/outputs
  - [x] Stdout display
  - [ ] Code editor js library
  - [ ] Solution to the input/output assignment issue: You can modify shared variables in the `exec` scope, but can't re-assign them. Assignment just creates a new local variable in the `exec` scope (which then as a result loses a way to reference the shared variable). Possible solutions:
    - Closures-esque solution
      - Create a closure that takes in the shared variables and returns a function that can access them
      - Pass the closure
    - ❌ ~~Make the shared variable an attribute of a singleton instance and overload the `__setattr__` method of that class~~
      - *FAILED*: It just doesn't work for some reason. The assignment still just creates a new local variable in the `exec` scope instead of being caught by the overloaded `__setattr__` method of the singleton. No idea why. 
    - Regex replace assignments with setter method calls
    - Create new method to replace assignments and leave it to the user to use it
- [ ] Decide whether to try to splice/parse `return` statements and values and dynamically add them to UI in real-time 
- [ ] Test core features
- [ ] Document
- [ ] Finalize version without the tensor wrapper
- [ ] Consider actual use cases and functionality and then deicde whether to finish the tensor wrapper class. If implementing:
  - [ ] Make optional
  - [ ] Document
  - [ ] Test
- [ ] Re-evaluate [Possible Features](#possible-features) and update plan


# Example Uses

## Accessing Stateful Variables at Time of Node Execution

#### Get the most recent image in a folder

```python
import os
import random

files = os.listdir("/path/to/folder")
files.sort(key=os.path.getmtime)

# Choose a random second image with the condition that it must be the same size
sample_files = [f for f in files if os.path.getsize(f) == os.path.getsize(files[1])]
paired_file = random.choice(sample_files)

image2.to(paired_file) # Wrapper class will handle conversion to tensor automatically
```

## Type Conversion

#### Convert between Number Types with Printed Debug Info

```python
print(f"The type of number1 when it was received was {type(number1)}")

if str(number1).isnumeric():
    number1.to(int(number1))
else:
    print(f"number1 was not a number. It was {number1}")

# Maybe change to 0 if it's negative (e.g., you are padding image1 to match image2 size but image1 is larger than in one dimension)
if number1 < 0:
    number1.to(0)
```

#### Color Format Conversion that Always Works



```python
import cv2
hex_color = text1 # text1 is the first text input in the node

def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# We can even add type checks to prevent frustration or inconsistencies with other node outputs
if not isinstance(hex_color, str):
    hex = str(hex_color)

red, green, blue = hex_to_rgb(hex_color)

# Output integer values representing r, g, b
number1.to(int(red))
number2.to(int(green))
number3.to(int(blue))
```




## Image Manipulation

## Debugging


## Logical Operators / Conditional Execution


## Math


## Scripts for Specific Workflow Tasks

#### Get Complementary Colors from an Image

```python
from sklearn.cluster import KMeans

pixels = image1.view(-1, image1.shape[-1]).numpy() # torch already imported
kmeans = KMeans(n_clusters=2, random_state=0).fit(pixels)
main_colors = kmeans.cluster_centers_
complement_colors = [(255 - main_colors[i]) % 256 for i in range(main_colors.shape[0])]

# text1 and text2 are output values. Re-assign them to desired value and then pipe the output in the UI
text1.to(complement_colors[0])
text2.to(complement_colors[1])
```

#### Combine Dynamic Values with Wildcards for Prompt Generation

We may have good tools involving wildcards, but perhaps some tokens in the prompt should be dynamically generated (like from determining the complementary color), while the rest can be wildcards.

```python
import random

# Assume you put the colors from the previous example into the text1 input for this node
complementary_color = text1

prompt = f"A {complementary_color} __wildcard_obj___ __wildcard_action__ in __wildcard_location__"

# Now take the text2 output and pipe to a wildcard node
text2.to(prompt)
```


