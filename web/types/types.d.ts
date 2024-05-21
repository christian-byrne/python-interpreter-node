import { LGraphNode, IWidget } from "@comfy-main-web/types/litegraph.js";

// --------------------------------------------------------------
// From comfy_mtb:

export interface ComfyApp {
  graph: LGraph;
  queueItems?: { number: number; batchCount: number }[];
  processingQueue?: boolean;
  ui: ComfyUI;
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
  addDOMWidget?: (
    name: string,
    type: string,
    element: Element,
    options: Record<string, unknown>
  ) => IWidget;
  onNodeCreated?: () => void;
  getExtraMenuOptions?: () => ContextMenuItem[];
  onExecuted?: (data: {
    text: string[];
    value?: string;
    string?: string;
  }) => void;

  nodeData?: NodeData;
  category?: str;
  comfyClass?: str;
  widgets?: ComfyWidget[];
}

export type NodeType = typeof LGraphNodeExtension;

// --------------------------------------------------------------

export interface WidgetOptions extends Record<string, any> {
  getValue: () => any;
  setValue?: (value: any) => void;

  hideOnZoomOut?: boolean;
  selection?: string[];
  max?: number;
  min?: number;
  precision?: number;
  round?: number;
  step?: number;

  on?: string;
  off?: string;
}

export interface ComfyWidget extends IWidget {
  onRemove?: () => void;

  value?: any;
  options: WidgetOptions;
  last_y?: number;
  computedHeight?: number;
  element?: HTMLElement;
  inputEl?: HTMLInputElement;
}
