export const nodeConfig = {
    nodeTitle: "Python Interpreter",
    projectDirName: "python-interpreter-node",
    nodeBackendName: "Exec Python Code Script",
    graphName: "Python Interpreter Node",
    codeEditorId: "python_code",
    hiddenInputId: "raw_code",
    aceScriptId: "ace-script-python-interpreter-node",
    stdoutErrId: "output_text",
    placeholderCode: `"""Docs: https://github.com/christian-byrne/python-interpreter-node"""

# Use .to() to re-assign the value of input/output variables
list1.to([1, 2, 3]) # Instead of list1 = [1, 2, 3]
number1.to(3.14) # Instead of number1 = 3.14

# If passing inputs/outputs as args to non-builtins, use .data
from torchvision.transforms import ToPILImage
image1.to(image1.squeeze(0).permute(2, 0, 1)) # From BHWC to CHW
image1_pil = ToPILImage()(image1.data) # Use .data when passing as arg
image1.to(image1.permute(1, 2, 0).unsqueeze(0)) # Back to BHWC

# In all other cases, code behaves like normal python code
# Any variables you define yourself will behave as expected
print(image1, image2, mask1, mask2, number1, number2, sep='\\n')
print(text1, text2, dict1, dict2, list1, list2, sep='\\n')

`,
};
