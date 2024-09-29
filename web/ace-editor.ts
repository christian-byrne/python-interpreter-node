import { Ace } from "./types/ace.js";
import { getWorkflowNodeByName } from "./get-workflow-data.js";
import { nodeConfig } from "./config.js";
import { LGraphNodeExtension } from "./types/comfy-app.js";

declare var ace: Ace;

export async function initAceInstance() {
  try {
    setTimeout(() => {
      if (ace?.edit) {
        console.debug(
          "[onNodeCreated handler] Initializing ace editor for python code node"
        );
        let editor = ace.edit(nodeConfig.codeEditorId);
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
        ace.require("ace/ext/searchbox");
      }
    }, 128);
  } catch (e) {
    console.debug(
      "[onNodeCreated handler] Error trying to initialize ace editor for python code node",
      e
    );
  }

  // Load code from workflow into editor. Call aftering rendering so all node props are defined.
  let savedSession: boolean = false;
  const workflow = await getWorkflowNodeByName(nodeConfig.nodeBackendName);
  if (workflow) {
    // The raw_code widget is the hidden input widget at position 0 (top)
    const persistentCode = workflow?.widgets_values[0];
    if (
      persistentCode &&
      persistentCode.replace(/\s/g, "") !== "" &&
      persistentCode !== nodeConfig.placeholderCode
    ) {
      console.info(
        "[setup] Persistent Python Code session detected. Loading from history"
      );
      savedSession = !savedSession;
      ace.edit(nodeConfig.codeEditorId).setValue(persistentCode);
    }
    if (!savedSession) {
      ace.edit(nodeConfig.codeEditorId).setValue(nodeConfig.placeholderCode);
    }
  }
}

export async function createAceDomElements(node: LGraphNodeExtension) {
  const acePythonContainer = Object.assign(document.createElement("div"), {
    id: nodeConfig.codeEditorId,
    textContent: nodeConfig.placeholderCode, // most likely can remove this
    style: {
      width: "100%",
      height: "100%",
      position: "relative",
    },
  });

  // Add ace editor container to the node on creation
  if (node.addDOMWidget !== undefined) {
    node.addDOMWidget(
      nodeConfig.codeEditorId,
      "customtext",
      acePythonContainer,
      {
        getValue: function () {
          try {
            if (ace?.edit) {
              return ace.edit(nodeConfig.codeEditorId).getValue();
            }
          } catch (e) {
            console.debug(
              "[onNodeCreated handler] Error trying to get value from ace editor for python code node",
              e
            );
          }
        },
      }
    );
  }

  // Mirror code editor text to hidden input widget
  if (ace?.edit) {
    ace
      .edit(nodeConfig.codeEditorId)
      .getSession()
      .on("change", (e: Event) => {
        node.widgets.find((w) => w.name === nodeConfig.hiddenInputId).value =
          ace.edit(nodeConfig.codeEditorId).getValue();
      });
  }
}
