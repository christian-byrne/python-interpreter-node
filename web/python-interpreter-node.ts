import { app } from "@comfy-main-web/scripts/app.js";
import {
  ComfyExtension,
  ComfyObjectInfo,
} from "@comfy-main-web/types/comfy.js";
import { LGraph } from "@comfy-main-web/types/litegraph.js";
import { ComfyApp, NodeType, LGraphNodeExtension } from "./types/comfy-app.js";
import { Ace } from "./types/ace.js";
import { initAceInstance, createAceDomElements } from "./ace-editor.js";
import { appendStdoutWidget } from "./append-stdout.js";
import { nodeConfig } from "./config.js";

declare var ace: Ace;

const PythonInterpreterExtension: ComfyExtension = {
  name: nodeConfig.graphName,
  init: async (app: ComfyApp) => {
    document.head.append(
      Object.assign(document.createElement("script"), {
        src: nodeConfig.aceLibPath,
      })
    );
  },
  beforeRegisterNodeDef: async (
    nodeType: NodeType,
    nodeData: ComfyObjectInfo,
    app: ComfyApp
  ) => {
    if (nodeData?.name == nodeConfig.nodeBackendName) {
      const constructorPrototype = nodeType.prototype;
      const liteGraph: LGraph = app.graph;

      // Create ace-editor DOM elements and listeners.
      constructorPrototype.onNodeCreated = function () {
        const node: LGraphNodeExtension = this;
        console.debug("[onNodeCreated Handler] Node created:", node);
        if (node.title == nodeConfig.nodeTitle) {
          initAceInstance();
          createAceDomElements(node);
        }
      };

      // Add a new widget to display the stdout/stderr after execution.
      constructorPrototype.onExecuted = function (data) {
        const node: LGraphNodeExtension = this;
        console.debug("[onExecuted handler] Node executed:", node);
        if (node.widgets) {
          appendStdoutWidget(node, liteGraph, data);
        }
      };
    }
  },
};

app.registerExtension(PythonInterpreterExtension);
