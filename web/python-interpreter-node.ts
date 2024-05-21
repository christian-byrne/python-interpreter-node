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
list1.to([1, 2, 3, 4])
number1.to(3.14)

# If passing inputs/outputs as args to non-builtins, use .data
from torchvision.transforms import ToPILImage
image1.to(image1.squeeze(0).permute(2, 0, 1)) # From BHWC to CHW
image1_pil = ToPILImage()(image1.data) # Use .data when passing as arg
image1_pil.show()"
image1.to(image1.permute(1, 2, 0).unsqueeze(0)) # Back to BHWC

# In all other cases, code behaves like normal python code
# Any variables you define yourself will behave as expected
print(image1, image2, mask1, mask2, number1, number2, sep='\\n')
print(text1, text2, dict1, dict2, list1, list2, sep='\\n')`;

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
  nodeCreated: async (node: LGraphNodeExtension, app: ComfyApp) => {
    if (node?.widgets) {
      const acePython = Object.assign(document.createElement("div"), {
        id: "python_code",
        textContent: PLACEHOLDER_CODE,
        style: {
          width: "300px",
          height: "300px",
        },
      });

      if (node.addDOMWidget !== undefined) {
        node.addDOMWidget("python_code", "customtext", acePython, {
          getValue: () => acePython.textContent,
          hideOnZoom: true,
          type: "customtext",
          value: acePython.textContent,
        });
      }

      if (ace) {
        const editor = ace.edit("python_code");
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
      } else {
        console.error("ace not loaded");
      }
    }
    // }
  },
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
    if (nodeData.name == "Exec Python Code Script") {
      nodeType.prototype.onExecuted = function (data) {
        if (!this.widgets) {
          return;
        }

        const insertIndex = this.widgets.findIndex(
          (w) => w.name === "output_text"
        );
        if (insertIndex !== -1) {
          for (let i = insertIndex; i < this.widgets.length; i++) {
            this.widgets[i].onRemove?.();
          }
          this.widgets.length = insertIndex;
        }

        const outputWidget = ComfyWidgets["STRING"](
          this,
          "output_text",
          ["STRING", { multiline: true }],
          app
        ).widget;
        outputWidget.value = data.text.join("");
      };
    }
  },
};

app.registerExtension(PythonInterpreterNode);
