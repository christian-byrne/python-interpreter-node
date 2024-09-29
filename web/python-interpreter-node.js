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
            src: nodeConfig.aceLibPath,
        }));
    }),
    beforeRegisterNodeDef: (nodeType, nodeData, app) => __awaiter(void 0, void 0, void 0, function* () {
        if ((nodeData === null || nodeData === void 0 ? void 0 : nodeData.name) == nodeConfig.nodeBackendName) {
            const constructorPrototype = nodeType.prototype;
            const liteGraph = app.graph;
            // Create ace-editor DOM elements and listeners.
            constructorPrototype.onNodeCreated = function () {
                const node = this;
                console.debug("[onNodeCreated Handler] Node created:", node);
                if (node.title == nodeConfig.nodeTitle) {
                    initAceInstance();
                    createAceDomElements(node);
                }
            };
            // Add a new widget to display the stdout/stderr after execution.
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
