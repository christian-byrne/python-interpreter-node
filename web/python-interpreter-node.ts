import { app } from "@comfy-main-web/scripts/app.js";
import { ComfyWidgets } from "@comfy-main-web/scripts/widgets.js";
import {
  ComfyExtension,
  ComfyObjectInfo,
} from "@comfy-main-web/types/comfy.js";
import { ComfyApp, NodeType, LGraphNodeExtension } from "./types/types.js";
declare var ace: any;

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

const PythonInterpreterNode: ComfyExtension = {
  name: "PythonInterpreter",
  init: async (app: ComfyApp) => {
    document.head.append(
      Object.assign(document.createElement("script"), {
        src: "https://cdn.jsdelivr.net/npm/ace-builds@1.33.3/src-min-noconflict/ace.js",
      })
    );
  },
  setup: async (app: ComfyApp) => {},
  getCustomWidgets: async (app: ComfyApp) => {
    return {
      STRING: ComfyWidgets["STRING"],
    };
  },
  loadedGraphNode: async (node: LGraphNodeExtension, app: ComfyApp) => {},
  nodeCreated: async (node: LGraphNodeExtension, app: ComfyApp) => {},
  addCustomNodeDefs: async (
    defs: Record<string, ComfyObjectInfo>,
    app: ComfyApp
  ) => {},
  registerCustomNodes: async (app: ComfyApp) => {},
  beforeRegisterNodeDef: async (
    nodeType: NodeType,
    nodeData: ComfyObjectInfo,
    app: ComfyApp
  ) => {
    if (nodeData?.name == "Exec Python Code Script") {
      const prototype = nodeType.prototype;

      prototype.onNodeCreated = async function () {
        // Create the ace editor container
        const acePythonContainer = Object.assign(
          document.createElement("div"),
          {
            id: "python_code",
            textContent: PLACEHOLDER_CODE,
            style: {
              width: "300px",
              height: "300px",
            },
          }
        );

        // Add the ace editor container to the node
        if (this.addDOMWidget !== undefined) {
          this.addDOMWidget("python_code", "customtext", acePythonContainer, {
            getValue: function () {
              return ace.edit("python_code").getValue();
            },
          });
        }

        // Initialize the ace editor instance asynchronously
        try {
          if (ace) {
            let editor = ace.edit("python_code");
            await editor.setOptions({
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
        } catch (e) {
          console.error(
            "Error trying to initialize ace editor for python code node",
            e
          );
        }

        const x = this;

        // Add a listener to the canvas element to update the hidden input widget with the ace editor content on keydown
        app.canvasEl.addEventListener("keydown", (e) => {
          // Remove any displayed raw_code widgets
          let keepNodesCount = 1;
          const recursiveRemoveWidgets = (widgets, curIndex) => {
            if (curIndex === -1) {
              return;
            }
            if (widgets[curIndex].name === "raw_code") {
              widgets[curIndex].onRemove?.();
            } else {
              keepNodesCount++;
            }
            curIndex--;
            recursiveRemoveWidgets(widgets, curIndex);
          };

          recursiveRemoveWidgets(this.widgets, this.widgets.length - 1);
          this.widgets.length = keepNodesCount;

          // If ENTER, append a new version of the raw_code widget with the updated ace editor content
          if (e.key !== "Enter") {
            return;
          }
          const outputWidget = ComfyWidgets["STRING"](
            this,
            "raw_code",
            ["STRING", { multiline: true }],
            app
          ).widget;
          outputWidget.value = ace.edit("python_code").getValue();
          // outputWidget.onResize?.(0);
          // console.log(outputWidget);
          console.log(this.widgets);
          requestAnimationFrame(() => {
            const size_ = x.computeSize();
            console.log(size_);
            if (size_[0] < x.size[0]) {
              size_[0] = x.size[0];
            }
            if (size_[1] < x.size[1]) {
              size_[1] = x.size[1];
            }
            x.onResize?.(size_);
            app.graph.setDirtyCanvas(true, false);
          });
          // x.onResize?.(2);
        });
      };

      // After execution, add a new widget to display the stdout/stderr
      prototype.onExecuted = function (data) {
        if (!this.widgets) {
          return;
        }

        // Remove existing stderror/stdout widget if it exists
        const insertIndex = this.widgets.findIndex(
          (w) => w.name === "output_text"
        );
        if (insertIndex !== -1) {
          for (let i = insertIndex; i < this.widgets.length; i++) {
            this.widgets[i].onRemove?.();
          }
          this.widgets.length = insertIndex;
        }

        // Construct new widget with the output text and set value to stdout/stderr
        const outputWidget = ComfyWidgets["STRING"](
          this,
          "output_text",
          ["STRING", { multiline: true }],
          app
        ).widget;
        outputWidget.value = data.text.join("");
        outputWidget.element.style.height = "3px";

        requestAnimationFrame(() => {
          const size_ = this.computeSize();
          if (size_[0] < this.size[0]) {
            size_[0] = this.size[0];
          }
          if (size_[1] < this.size[1]) {
            size_[1] = this.size[1];
          }
          this.onResize?.(size_);
          app.graph.setDirtyCanvas(true, false);
        });
      };
    }
  },
};

app.registerExtension(PythonInterpreterNode);
