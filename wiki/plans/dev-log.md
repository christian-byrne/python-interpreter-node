# Plan

- [ ] Finish core features
  - [x] Code execution
    - [x] Error hints and tracebacks
  - [ ] Dynamic inputs/outputs
  - [x] Stdout display
  - [ ] Code editor js library
  - [x] Solution to the input/output assignment issue: You can modify shared variables in the `exec` scope, but can't re-assign them. Assignment just creates a new local variable in the `exec` scope (which then as a result loses a way to reference the shared variable). Possible solutions:
    - ❌ - ~~Create a closure that takes in the shared variables and returns a function that can access them~~
    - ✅ Make the shared variable an attribute of a singleton instance and overload the `__setattr__` method of that class
    - ❌ ~~Regex replace assignments with setter method calls~~
    - ❌ ~~Create new method to replace assignments and leave it to the user to use it~~
- [x] Decide whether to try to splice/parse `return` statements and values and dynamically add them to UI in real-time 
- [ ] Test core features
- [ ] Document
- [x] Consider actual use cases and functionality and then deicde whether to finish the tensor wrapper class. If implementing:
  - [x] ~~Make opt-out option~~
  - [x] ~~Document~~
  - [x] ~~Test~~
- [ ] Re-evaluate [Possible Features](#possible-features) and update plan


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

## Non-Urgent TODO

- [x] Refactor file structure
- [ ] Add some `ANY` inputs/outputs (type `ANY`, names `any1`, `any2`). Add some common custom types and wrappers for them
- [ ] Add generalized/generic wrapper
- [ ] Add wrappers/inputs for the other builtin types like `LATENT`