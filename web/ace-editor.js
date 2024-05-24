var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { getWorkflowNodeByName } from "./get-workflow-data.js";
import { nodeConfig } from "./config.js";
export function initAceInstance() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            if (ace === null || ace === void 0 ? void 0 : ace.edit) {
                console.debug("[onNodeCreated handler] Initializing ace editor for python code node");
                let editor = ace.edit(nodeConfig.codeEditorId);
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
                });
            }
        }
        catch (e) {
            // TODO: handle error
            console.error("[onNodeCreated handler] Error trying to initialize ace editor for python code node", e);
        }
        // Load code from workflow into editor. Call aftering rendering so all node props are defined.
        let savedSession = false;
        const workflow = yield getWorkflowNodeByName(nodeConfig.nodeBackendName);
        if (workflow) {
            // The raw_code widget is the hidden input widget at position 0 (top)
            const persistentCode = workflow === null || workflow === void 0 ? void 0 : workflow.widgets_values[0];
            if (persistentCode &&
                persistentCode.replace(/\s/g, "") !== "" &&
                persistentCode !== nodeConfig.placeholderCode) {
                console.info("[setup] Persistent Python Code session detected. Loading from history");
                savedSession = !savedSession;
                ace.edit(nodeConfig.codeEditorId).setValue(persistentCode);
            }
            if (!savedSession) {
                ace.edit(nodeConfig.codeEditorId).setValue(nodeConfig.placeholderCode);
            }
        }
    });
}
export function createAceDomElements(node) {
    return __awaiter(this, void 0, void 0, function* () {
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
            node.addDOMWidget(nodeConfig.codeEditorId, "customtext", acePythonContainer, {
                getValue: function () {
                    return ace.edit(nodeConfig.codeEditorId).getValue();
                },
            });
        }
        // Mirror code editor text to hidden input widget
        if (ace === null || ace === void 0 ? void 0 : ace.edit) {
            ace
                .edit(nodeConfig.codeEditorId)
                .getSession()
                .on("change", (e) => {
                node.widgets.find((w) => w.name === nodeConfig.hiddenInputId).value = ace.edit(nodeConfig.codeEditorId).getValue();
            });
        }
    });
}
