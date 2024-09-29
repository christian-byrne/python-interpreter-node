import { Ace } from "./types/ace.js";
import { nodeConfig } from "./config.js";
import { LGraphNodeExtension } from "./types/comfy-app.js";

declare var ace: Ace;

export async function initAceInstance(
  node: LGraphNodeExtension,
  editorId: string
) {
  try {
    setTimeout(() => {
      if (ace?.edit) {
        let editor = ace.edit(editorId);
        const savedCode = node?.widgets_values?.length
          ? node.widgets_values[0]
          : nodeConfig.placeholderCode;
        editor.setValue(savedCode);
        editor.setOptions({
          tabSize: 2,
          wrap: true,
          mode: "ace/mode/python",
          theme: "ace/theme/github_dark",
          showPrintMargin: false,
          showGutter: false,
          customScrollbar: true,
          enableAutoIndent: true,
        });
        ace.require("ace/ext/language_tools");
      }
    }, 128);
  } catch (e) {
    console.debug(
      "[onNodeCreated handler] Error trying to initialize ace editor for python code node",
      e
    );
  }
}

export async function createAceDomElements(
  node: LGraphNodeExtension,
  editorId: string
) {
  // Create ace editor container element
  const acePythonContainer = Object.assign(document.createElement("div"), {
    id: editorId,
    style: {
      width: "100%",
      height: "100%",
      position: "relative",
    },
  });

  // Add ace editor container to the node on creation
  if (node.addDOMWidget !== undefined) {
    node.addDOMWidget(editorId, "customtext", acePythonContainer, {
      getValue: function () {
        try {
          if (ace?.edit) {
            return ace.edit(editorId).getValue();
          }
        } catch (e) {
          console.debug(
            "[onNodeCreated handler] Error trying to get value from ace editor for python code node",
            e
          );
        }
      },
    });
  }

  // Mirror code editor text to hidden input widget
  try {
    if (ace?.edit) {
      ace
        .edit(editorId)
        .getSession()
        .on("change", (e: Event) => {
          node.widgets.find((w) => w.name === nodeConfig.hiddenInputId).value =
            ace.edit(editorId).getValue();
        });
    }
  } catch (e) {
    console.debug(
      "[onNodeCreated handler] Error trying to mirror code editor text to hidden input widget",
      e
    );
  }
}
