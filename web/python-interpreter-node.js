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
const PythonInterpreterExtension = {
    name: nodeConfig.graphName,
    init: (app) => __awaiter(void 0, void 0, void 0, function* () {
        document.head.append(Object.assign(document.createElement("script"), {
            src: "https://cdnjs.cloudflare.com/ajax/libs/ace/1.34.0/ace.min.js",
        }));
    }),
    setup: (app) => __awaiter(void 0, void 0, void 0, function* () {
        const nodeActive = app.graph.findNodeByTitle(nodeConfig.nodeTitle);
        if (nodeActive) {
            initAceInstance();
        }
    }),
    getCustomWidgets: (app) => __awaiter(void 0, void 0, void 0, function* () {
        return {};
    }),
    loadedGraphNode: (node, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    nodeCreated: (node, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    addCustomNodeDefs: (defs, app) => __awaiter(void 0, void 0, void 0, function* () { }),
    registerCustomNodes: (app) => __awaiter(void 0, void 0, void 0, function* () { }),
    beforeRegisterNodeDef: (nodeType, nodeData, app) => __awaiter(void 0, void 0, void 0, function* () {
        if ((nodeData === null || nodeData === void 0 ? void 0 : nodeData.name) == nodeConfig.nodeBackendName) {
            const constructorPrototype = nodeType.prototype;
            const liteGraph = app.graph;
            constructorPrototype.onNodeCreated = function () {
                const node = this;
                console.debug("[onNodeCreated Handler] Node created:", node);
                if (node.title == nodeConfig.nodeTitle) {
                    createAceDomElements(node);
                }
            };
            constructorPrototype.onExecuted = function (data) {
                const node = this;
                console.debug("[onExecuted handler] Node executed:", node);
                if (node.widgets) {
                    appendStdoutWidget(node, liteGraph, data);
                }
            };
        }
    }),
};
app.registerExtension(PythonInterpreterExtension);
