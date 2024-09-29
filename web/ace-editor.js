var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { nodeConfig } from "./config.js";
export function initAceInstance(node, editorId) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            setTimeout(() => {
                var _a;
                if (ace === null || ace === void 0 ? void 0 : ace.edit) {
                    let editor = ace.edit(editorId);
                    const savedCode = ((_a = node === null || node === void 0 ? void 0 : node.widgets_values) === null || _a === void 0 ? void 0 : _a.length)
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
        }
        catch (e) {
            console.debug("[onNodeCreated handler] Error trying to initialize ace editor for python code node", e);
        }
    });
}
export function createAceDomElements(node, editorId) {
    return __awaiter(this, void 0, void 0, function* () {
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
                        if (ace === null || ace === void 0 ? void 0 : ace.edit) {
                            return ace.edit(editorId).getValue();
                        }
                    }
                    catch (e) {
                        console.debug("[onNodeCreated handler] Error trying to get value from ace editor for python code node", e);
                    }
                },
            });
        }
        // Mirror code editor text to hidden input widget
        try {
            if (ace === null || ace === void 0 ? void 0 : ace.edit) {
                ace
                    .edit(editorId)
                    .getSession()
                    .on("change", (e) => {
                    node.widgets.find((w) => w.name === nodeConfig.hiddenInputId).value =
                        ace.edit(editorId).getValue();
                });
            }
        }
        catch (e) {
            console.debug("[onNodeCreated handler] Error trying to mirror code editor text to hidden input widget", e);
        }
    });
}
