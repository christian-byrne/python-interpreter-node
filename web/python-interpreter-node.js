var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";
const PLACEHOLDER_CODE = `"""Docs: https://github.com/christian-byrne/python-interpreter-node"""

# Use .to() to re-assign the value of input/output variables
list1.to([1, 2, 3]) # Instead of list1 = [1, 2, 3]
number1.to(3.14) # Instead of number1 = 3.14

# If passing inputs/outputs as args to non-builtins, use .data
from torchvision.transforms import ToPILImage
image1.to(image1.squeeze(0).permute(2, 0, 1)) # From BHWC to CHW
image1_pil = ToPILImage()(image1.data) # Use .data when passing as arg
image1_pil.show()
image1.to(image1.permute(1, 2, 0).unsqueeze(0)) # Back to BHWC

# In all other cases, code behaves like normal python code
# Any variables you define yourself will behave as expected
print(image1, image2, mask1, mask2, number1, number2, sep='\\n')
print(text1, text2, dict1, dict2, list1, list2, sep='\\n')


`;
const PythonInterpreterNode = {
    name: "PythonInterpreter",
    init: (app) => __awaiter(void 0, void 0, void 0, function* () {
        document.head.append(Object.assign(document.createElement("script"), {
            src: "https://cdn.jsdelivr.net/npm/ace-builds@1.33.3/src-min-noconflict/ace.js",
        }));
    }),
    setup: (app) => __awaiter(void 0, void 0, void 0, function* () { }),
    getCustomWidgets: (app) => __awaiter(void 0, void 0, void 0, function* () {
        return {};
    }),
    loadedGraphNode: (node, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    nodeCreated: (node, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    addCustomNodeDefs: (defs, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    registerCustomNodes: (app) => __awaiter(void 0, void 0, void 0, function* () { }),
    beforeRegisterNodeDef: (nodeType, nodeData, app) => __awaiter(void 0, void 0, void 0, function* () {
        if ((nodeData === null || nodeData === void 0 ? void 0 : nodeData.name) == "Exec Python Code Script") {
            const prototype = nodeType.prototype;
            prototype.onNodeCreated = function () {
                console.log(this);
                // Create the ace editor container
                const acePythonContainer = Object.assign(document.createElement("div"), {
                    id: "python_code",
                    textContent: PLACEHOLDER_CODE,
                    style: {
                        width: "300px",
                        height: "300px",
                    },
                });
                // Add the ace editor container to the node
                if (this.addDOMWidget !== undefined) {
                    this.addDOMWidget("python_code", "customtext", acePythonContainer, {
                        getValue: function () {
                            if (!(ace === null || ace === void 0 ? void 0 : ace.edit))
                                return PLACEHOLDER_CODE;
                            return ace.edit("python_code").getValue();
                        },
                    });
                }
                // Initialize the ace editor instance asynchronously
                try {
                    if (ace === null || ace === void 0 ? void 0 : ace.edit) {
                        let editor = ace.edit("python_code");
                        editor.setOptions({
                            tabSize: 2,
                            useSoftTabs: true,
                            wrap: true,
                            mode: "ace/mode/python",
                            theme: "ace/theme/github_dark",
                            showPrintMargin: false,
                            showGutter: false,
                            customScrollbar: true,
                            enableAutoIndent: true,
                            enableKeyboardAccessibility: true,
                        });
                    }
                }
                catch (e) {
                    console.error("Error trying to initialize ace editor for python code node", e);
                }
                const x = this;
                // Add a listener to the canvas element to update the hidden input widget with the ace editor content on keydown
                app.canvasEl.addEventListener("keydown", (e) => {
                    var _a;
                    // Remove any displayed raw_code widgets
                    let keepNodesCount = 1;
                    const recursiveRemoveWidgets = (widgets, curIndex) => {
                        var _a, _b;
                        if (curIndex === -1) {
                            return;
                        }
                        if (widgets[curIndex].name === "raw_code" ||
                            widgets[curIndex].name === "output_text") {
                            (_b = (_a = widgets[curIndex]).onRemove) === null || _b === void 0 ? void 0 : _b.call(_a);
                        }
                        else {
                            keepNodesCount++;
                        }
                        curIndex--;
                        recursiveRemoveWidgets(widgets, curIndex);
                    };
                    recursiveRemoveWidgets(this.widgets, this.widgets.length - 1);
                    this.widgets.length = keepNodesCount;
                    // If ENTER, append a new version of the raw_code widget with the updated ace editor content
                    // if (e.key !== "Enter") {
                    //   return;
                    // }
                    const outputWidget = ComfyWidgets["STRING"](this, "raw_code", ["STRING", { multiline: true }], app).widget;
                    if (ace) {
                        outputWidget.value = ace.edit("python_code").getValue();
                    }
                    requestAnimationFrame(() => {
                        var _a;
                        const size_ = x.computeSize();
                        console.log(size_);
                        if (size_[0] < x.size[0]) {
                            size_[0] = x.size[0];
                        }
                        if (size_[1] < x.size[1]) {
                            size_[1] = x.size[1];
                        }
                        (_a = x.onResize) === null || _a === void 0 ? void 0 : _a.call(x, size_);
                        app.graph.setDirtyCanvas(true, false);
                    });
                    (_a = x.onResize) === null || _a === void 0 ? void 0 : _a.call(x, [100, 500]);
                });
            };
            // After execution, add a new widget to display the stdout/stderr
            prototype.onExecuted = function (data) {
                var _a, _b;
                if (!this.widgets) {
                    return;
                }
                // Remove existing stderror/stdout widget if it exists
                const insertIndex = this.widgets.findIndex((w) => w.name === "raw_code");
                if (insertIndex !== -1) {
                    for (let i = insertIndex; i < this.widgets.length; i++) {
                        (_b = (_a = this.widgets[i]).onRemove) === null || _b === void 0 ? void 0 : _b.call(_a);
                    }
                    this.widgets.length = insertIndex;
                }
                // Construct new widget with the output text and set value to stdout/stderr
                const outputWidget = ComfyWidgets["STRING"](this, "output_text", ["STRING", { multiline: true }], app).widget;
                outputWidget.value = data.text.join("");
                requestAnimationFrame(() => {
                    var _a;
                    const size_ = this.computeSize();
                    if (size_[0] < this.size[0]) {
                        size_[0] = this.size[0];
                    }
                    if (size_[1] < this.size[1]) {
                        size_[1] = this.size[1];
                    }
                    (_a = this.onResize) === null || _a === void 0 ? void 0 : _a.call(this, size_);
                    app.graph.setDirtyCanvas(true, false);
                });
            };
        }
    }),
};
app.registerExtension(PythonInterpreterNode);
