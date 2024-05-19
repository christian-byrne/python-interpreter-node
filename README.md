# Python Interpreter ComfyUI Node

Features Implemented so Far:
- [x] Code execution (5/16)
- [x] Input value modification and output (5/17)
- [x] Stdout/err display (5/19)
- [ ] Output value assignment/pipe (an output value not associated with an input)
- [ ] Code editor plugin
- [ ] Dynamic inputs/outputs
- [ ] Testing and Docs

### Description

- Allows you to write Python code in the textarea of the node which executes when the workflow is queued
- The stdout/stderr (e.g., prints, error tracebacks) are displayed in the node. 
- The input values can be accessed by their UI name. 
- The output values can be set by assigning to their UI-names.

![alt text](wiki/pictures/demos/p1-zoom.png)

![alt text](wiki/pictures/demos/p1.png)



### Uses

- Anything that can be done with Python code
- Saving mini scripts embedded into a workflow
- Converting types
- Doing math with input values
- Debugging
  - Testing custom nodes faster.


### Wrapper Class with Operator Overloading

![alt text](wiki/pictures/demos/p2.png)

- Wrapper class around tensors with operator overloading for doing common image manipulation tasks.
- The inputs need to be wrapped in a class either way, but might remove operator overloading





