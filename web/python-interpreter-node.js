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
import { initAceInstance, createAceDomElements } from "./ace-editor.js";
import { appendStdoutWidget } from "./append-stdout.js";
import { nodeConfig } from "./config.js";
const ACTIVE_EDITORS = {};
const createUniqueID = () => {
    let id = Math.random().toString(36).substring(2, 9);
    while (ACTIVE_EDITORS[id]) {
        id = Math.random().toString(36).substring(2, 9);
    }
    ACTIVE_EDITORS[id] = true;
    return id;
};
const PythonInterpreterExtension = {
    name: nodeConfig.graphName,
    init: (app) => __awaiter(void 0, void 0, void 0, function* () {
        document.head.append(Object.assign(document.createElement("script"), {
            src: nodeConfig.aceLibPath,
        }));
    }),
    setup: (app) => __awaiter(void 0, void 0, void 0, function* () {
        const themeSelection = app.ui.settings.addSetting({
            id: "PythonInterpreter.Theme",
            name: "Editor Theme",
            defaultValue: "github_dark",
            type: "combo",
            options: nodeConfig.themes,
        });
    }),
    nodeCreated: (node) => __awaiter(void 0, void 0, void 0, function* () {
        console.debug("[onNodeCreated Handler] Node created:", node);
    }),
    beforeRegisterNodeDef: (nodeType, nodeData, app) => __awaiter(void 0, void 0, void 0, function* () {
        if ((nodeData === null || nodeData === void 0 ? void 0 : nodeData.name) == nodeConfig.nodeBackendName) {
            const constructorPrototype = nodeType.prototype;
            const liteGraph = app.graph;
            constructorPrototype.onNodeCreated = function () {
                const nodePrototype = this;
                if (nodePrototype.title == nodeConfig.nodeTitle) {
                    const editorId = createUniqueID();
                    console.debug("[onNodeCreated Handler] Node created:", nodePrototype);
                    console.debug("[onNodeCreated Handler] Editor ID:", editorId);
                    initAceInstance(nodePrototype, editorId);
                    createAceDomElements(nodePrototype, editorId);
                }
            };
            constructorPrototype.onExecuted = function (data) {
                const node = this;
                if (node.widgets) {
                    appendStdoutWidget(node, liteGraph, data);
                }
            };
        }
    }),
};
app.registerExtension(PythonInterpreterExtension);
