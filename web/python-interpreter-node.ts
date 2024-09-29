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
const ACTIVE_EDITORS = {};

const createUniqueID = (): string => {
  let id = Math.random().toString(36).substring(2, 9);
  while (ACTIVE_EDITORS[id]) {
    id = Math.random().toString(36).substring(2, 9);
  }
  ACTIVE_EDITORS[id] = true;
  return id;
}

const PythonInterpreterExtension: ComfyExtension = {
  name: nodeConfig.graphName,
  init: async (app: ComfyApp) => {
    document.head.append(
      Object.assign(document.createElement("script"), {
        src: nodeConfig.aceLibPath,
      })
    );
  },
  setup : async (app: ComfyApp) => {
    const themeSelection = app.ui.settings.addSetting({
      id: "PythonInterpreter.Theme",
      name: "Editor Theme",
      defaultValue: "github_dark",
      type: "combo",
      options: nodeConfig.themes,
    })
  },
  nodeCreated: async (node: LGraphNodeExtension) => {
    console.debug("[onNodeCreated Handler] Node created:", node);
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
        const nodePrototype: LGraphNodeExtension = this;
        if (nodePrototype.title == nodeConfig.nodeTitle) {
          const editorId = createUniqueID();
          console.debug("[onNodeCreated Handler] Node created:", nodePrototype);
          console.debug("[onNodeCreated Handler] Editor ID:", editorId);
          initAceInstance(nodePrototype, editorId);
          createAceDomElements(nodePrototype, editorId);
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
