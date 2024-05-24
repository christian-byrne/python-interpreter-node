import {
  LGraph,
  LGraphNode,
  IWidget,
} from "@comfy-main-web/types/litegraph.js";
import { ComfyUI } from "../web/scripts/ui.js";
import { ComfyExtension } from "@comfy-main-web/types/comfy.js";
import { ContextMenuItem } from "@comfy-main-web/types/litegraph.js";
import { LGraphNodeExtended } from "./comfy-app.js";
import { WidgetOptions } from "./widgets.js";

// --------------------------------------------------------------
// Originally from comfy_mtb

export interface ComfyApp {
  graph: LGraph;
  queueItems?: { number: number; batchCount: number }[];
  processingQueue?: boolean;
  ui: ComfyUI;
  canvasEl: HTMLCanvasElement;
  extensions: ComfyExtension[];
  nodeOutputs: Record<string, unknown>;
  nodePreviewImages: Record<string, Image>;
  shiftDown: boolean;
  isImageNode?: (node: LGraphNodeExtended) => boolean;
  queuePrompt: (number: number, batchCount: number) => Promise<void>;
  /** Loads workflow data from the specified file*/
  handleFile: (file: File) => Promise<void>;
  registerExtension: (extension: ComfyExtension) => void;
}

export declare class LGraphNodeExtension extends LGraphNode {
  /**
   * Adds a DOM widget to the application.
   *
   * @param name - The name of the widget.
   * @param type - The type of the widget.
   * @param element - The DOM element that represents the widget.
   * @param options - Additional options for the widget.
   * @returns The created widget.
   */
  addDOMWidget?: (
    name: string,
    type: string,
    element: HTMLElement,
    options: WidgetOptions 
  ) => IWidget;
  onNodeCreated?: () => void;
  getExtraMenuOptions?: () => ContextMenuItem[];
  onExecuted?: (data: {
    text: string[];
    value?: string;
    string?: string;
  }) => void;
  onExecutionStart?: () => void;

  nodeData?: NodeData;
  category?: str;
  comfyClass?: str;
  widgets?: ComfyWidget[];
}

export type NodeType = typeof LGraphNodeExtension;