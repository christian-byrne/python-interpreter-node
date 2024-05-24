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
        src: "https://cdn.jsdelivr.net/npm/ace-builds@1.33.3/src-min-noconflict/ace.js",
      })
    );
  },
  setup: async (app: ComfyApp) => {
    initAceInstance();
  },
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
    if (nodeData?.name == nodeConfig.nodeBackendName) {
      const constructorPrototype = nodeType.prototype; // See: https://www.typescriptlang.org/play/?#code/FDDGBsEMGdoAgDIHEBOkAOALAcgewCYCmcA3nMHJXAPTVwAiuh0AdgOQAucmkAbsbhYBRAB6FQAVw6F8cABSQWs3B0yEUcALaFVBaAEo4AIwCecIgDNIE8B2ABfEBYktQHAJaDjhC7hSEAJUIAc3doaRQ8InofORYCQgAVE3RCAC44DhTCXAtEVAwcBMMSCipaOAADLNTc-LQsKMJKuH8LdXgOXEy1esKmuFBBcJQJNz8AOjhEni5QRW84fhR3C3cZb3mJaEIyyhZCAHc4eKJk1Ll9AG4aOjkARkMTXAlBhe3iA+Ovdy4uwf8kGkcAW7hY4UUoF2VEGw1w4EIE3AuGCcgAhGjTklshN0CgVCpsoYKnIAEyGX7cGAguB4gk1Yh01IoLJ7cgwipY86IuldBlwMI9Rn4vnZOB1VTEZANIpEWHgjijcYoNkIubDRVjLooAAKIsJqTgAF44AB5IwAK3EHAmwR0evp2VNFjiCW5+jZQ3B8MRyNRXpGWr8DtFqQ9MIDPqRKLkAc1ypDBuIYIhrhyeQAYi43J4WOGqJ64Qjo6jzVa3BMwqJpOD3EYEbGNUrtYmGfpiXQAMJNoMaXlJt4sRaEEQ1oiyQ6-TAnI60-HoaBstkVGbC3ALkH+ODQHj+WSQUD42Ag8DgAUKyHMAGEIEbUw9IHy8K91U6VrG+SGI0APlIkeLfpyAARCO4hSDIQH6I4MJcji-YMhMgiiGB0iyCaKA3CuADKcCTqePT4sc6j4hoLgIseI5jn0jQJCAMJqjOhwAJIXmmH5fNRsqEJcVxsl8LGplCiHCGIkioZcDggMARg+H4gQhGEERNDELrSv0xTAEAA
      const liteGraph: LGraph = app.graph;

      // Create ace-editor DOM elements and listeners.
      constructorPrototype.onNodeCreated = function () {
        const node: LGraphNodeExtension = this;
        console.debug("[onNodeCreated Handler] Node created:", node);
        if (node.title == nodeConfig.nodeTitle) {
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
