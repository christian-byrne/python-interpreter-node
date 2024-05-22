import { app } from "@comfy-main-web/scripts/app.js";
import { ComfyWidgets } from "@comfy-main-web/scripts/widgets.js";
import {
  ComfyExtension,
  ComfyObjectInfo,
} from "@comfy-main-web/types/comfy.js";
import {
  ComfyApp,
  NodeType,
  LGraphNodeExtension,
  ComfyWidget,
  ComfyWidgetUIWrapper,
} from "./types/types.js";
import { LGraph } from "@comfy-main-web/types/litegraph.js";
declare var ace: any;

const PI_NODE_TITLE = "Python Interpreter";
const PI_NODE_BACKEND_NAME = "Exec Python Code Script";
const PI_LG_NAME = "Python Interpreter Node";
const CODE_EDITOR_ID = "python_code";
const HIDDEN_INPUT_ID = "raw_code";
const STDOUT_ERR_ID = "output_text";
const PI_PLACEHOLDER_CODE = `"""Docs: https://github.com/christian-byrne/python-interpreter-node"""

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

const PythonInterpreterExtension: ComfyExtension = {
  name: PI_LG_NAME,
  init: async (app: ComfyApp) => {
    document.head.append(
      Object.assign(document.createElement("script"), {
        src: "https://cdn.jsdelivr.net/npm/ace-builds@1.33.3/src-min-noconflict/ace.js",
      })
    );
  },
  setup: async (app: ComfyApp) => {},
  getCustomWidgets: async (app: ComfyApp) => {
    return {};
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
    if (nodeData?.name == PI_NODE_BACKEND_NAME) {
      const constructorPrototype = nodeType.prototype; // See: https://www.typescriptlang.org/play/?#code/FDDGBsEMGdoAgDIHEBOkAOALAcgewCYCmcA3nMHJXAPTVwAiuh0AdgOQAucmkAbsbhYBRAB6FQAVw6F8cABSQWs3B0yEUcALaFVBaAEo4AIwCecIgDNIE8B2ABfEBYktQHAJaDjhC7hSEAJUIAc3doaRQ8InofORYCQgAVE3RCAC44DhTCXAtEVAwcBMMSCipaOAADLNTc-LQsKMJKuH8LdXgOXEy1esKmuFBBcJQJNz8AOjhEni5QRW84fhR3C3cZb3mJaEIyyhZCAHc4eKJk1Ll9AG4aOjkARkMTXAlBhe3iA+Ovdy4uwf8kGkcAW7hY4UUoF2VEGw1w4EIE3AuGCcgAhGjTklshN0CgVCpsoYKnIAEyGX7cGAguB4gk1Yh01IoLJ7cgwipY86IuldBlwMI9Rn4vnZOB1VTEZANIpEWHgjijcYoNkIubDRVjLooAAKIsJqTgAF44AB5IwAK3EHAmwR0evp2VNFjiCW5+jZQ3B8MRyNRXpGWr8DtFqQ9MIDPqRKLkAc1ypDBuIYIhrhyeQAYi43J4WOGqJ64Qjo6jzVa3BMwqJpOD3EYEbGNUrtYmGfpiXQAMJNoMaXlJt4sRaEEQ1oiyQ6-TAnI60-HoaBstkVGbC3ALkH+ODQHj+WSQUD42Ag8DgAUKyHMAGEIEbUw9IHy8K91U6VrG+SGI0APlIkeLfpyAARCO4hSDIQH6I4MJcji-YMhMgiiGB0iyCaKA3CuADKcCTqePT4sc6j4hoLgIseI5jn0jQJCAMJqjOhwAJIXmmH5fNRsqEJcVxsl8LGplCiHCGIkioZcDggMARg+H4gQhGEERNDELrSv0xTAEAA
      const liteGraph: LGraph = app.graph;

      constructorPrototype.onNodeCreated = function () {
        const node: LGraphNodeExtension = this;
        console.debug("[onNodeCreated Handler] Node created:", node);
        if (node.title !== PI_NODE_TITLE) {
          return;
        }

        const acePythonContainer = Object.assign(
          document.createElement("div"),
          {
            id: CODE_EDITOR_ID,
            textContent: PI_PLACEHOLDER_CODE,
            style: {
              width: "300px",
              height: "500px",
            },
          }
        );

        // Add ace editor container to the node on creation
        if (node.addDOMWidget !== undefined) {
          node.addDOMWidget(CODE_EDITOR_ID, "customtext", acePythonContainer, {
            // Is this necessary?
            getValue: function () {
              return ace.edit(CODE_EDITOR_ID).getValue();
            },
          });
        }

        // TODO: use faster way to load
        // Initialize the ace editor object instance (TODO: asynchronously)
        try {
          if (ace?.edit) {
            console.debug("Initializing ace editor for python code node");
            let editor = ace.edit(CODE_EDITOR_ID);
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
        } catch (e) {
          // TODO: handle error
          console.error(
            "Error trying to initialize ace editor for python code node",
            e
          );
        }

        console.debug(
          "Adding keydown listener to canvas element to update hidden input widget with ace editor code"
        );
        app.canvasEl.addEventListener("keydown", (e) => {
          const keepWidgets: ComfyWidget[] = [];
          const removeWidgets: ComfyWidget[] = [];
          const initialWidgetsLength = node.widgets.length;

          const recursiveWidgetFilter = (
            widgets: ComfyWidget[],
            curIndex: number
          ) => {
            if (curIndex === widgets.length) {
              return;
            }
            const widget: ComfyWidget = widgets[curIndex];
            if (
              widget.name === HIDDEN_INPUT_ID ||
              widget.name === STDOUT_ERR_ID
            ) {
              removeWidgets.push(widget);
            } else {
              keepWidgets.push(widget);
            }
            recursiveWidgetFilter(widgets, curIndex + 1);
          };
          recursiveWidgetFilter(node.widgets, 0);
          console.debug(
            `Went from ${initialWidgetsLength} to ${keepWidgets.length} widgets`
          );
          console.debug(
            "Keeping widgets:",
            keepWidgets,
            "Removing widgets:",
            removeWidgets
          );
          node.widgets = keepWidgets;
          liteGraph.setDirtyCanvas(true, true);
          console.debug("After removal, node.widgets:", node.widgets);

          console.debug(
            "Triggering `onRemove` of widget in removeWidgets array"
          );
          for (let i = 0; i < removeWidgets.length; i++) {
            removeWidgets[i].onRemove?.();
            liteGraph.setDirtyCanvas(true, true);
          }

          // TODO: Be selective about the event types being targeted
          console.debug(`Creating new ${HIDDEN_INPUT_ID} widget`);
          const widgetWrapper: ComfyWidgetUIWrapper = ComfyWidgets["STRING"](
            node,
            HIDDEN_INPUT_ID,
            ["STRING", { multiline: true }],
            app
          );
          const outputWidget: ComfyWidget = widgetWrapper.widget;
          try {
            console.debug(
              `Setting hidden ${HIDDEN_INPUT_ID} widget's style to hidden`
            );
            outputWidget.element.style.display = "none";
            outputWidget.element.style.visibility = "hidden";
            outputWidget.element.style.opacity = "0";
            liteGraph.setDirtyCanvas(true, true);
          } catch (e) {
            console.error(
              `Error trying to set ${HIDDEN_INPUT_ID} widget's stlye (hiding)`,
              e
            );
          }

          try {
            console.debug("Setting output widget's value to ace editor value");
            // if (Object.getOwnPropertyNames(window).includes("ace")) {
            if (ace?.edit) {
              outputWidget.value = ace.edit("python_code").getValue();
            }
          } catch (e) {
            console.error("Error trying to get ace editor value", e);
          }
        });
      };

      // After execution, add a new widget to display the stdout/stderr
      constructorPrototype.onExecuted = function (data) {
        // TODO: Add type for data
        const node: LGraphNodeExtension = this;
        console.debug("[onExecuted handler] Node executed:", node);
        if (!node.widgets) {
          console.debug("No widgets found on node, skipping...");
          return;
        }

        const insertIndex = node.widgets.findIndex(
          (w) => w.name === STDOUT_ERR_ID
        );
        console.debug(
          `Insert index for ${STDOUT_ERR_ID} widget: ${insertIndex}`
        );
        if (insertIndex !== -1) {
          console.debug(
            `Removing existing ${STDOUT_ERR_ID} widgets after insert index`
          );
          for (let i = insertIndex; i < node.widgets.length; i++) {
            node.widgets[i].onRemove?.();
          }
          node.widgets.length = insertIndex;
        } else {
          console.debug(
            `No existing ${STDOUT_ERR_ID} widgets found. Nothing to remove...`
          );
        }

        console.debug(
          `Constructing new output_text widget with ${STDOUT_ERR_ID} data`
        );
        const outputWidget: ComfyWidget = ComfyWidgets["STRING"](
          node,
          STDOUT_ERR_ID,
          ["STRING", { multiline: true }],
          app
        ).widget;
        outputWidget.value = data.text.join("");
        liteGraph.setDirtyCanvas(true, true);
      };
    }
  },
};

app.registerExtension(PythonInterpreterExtension);
