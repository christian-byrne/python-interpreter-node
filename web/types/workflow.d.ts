type InputTypeName =
  | "IMAGE"
  | "MASK"
  | "STRING"
  | "INT"
  | "FLOAT"
  | "BOOLEAN"
  | "LATENT"
  | "MODEL"
  | "ANY"
  | string[]
  | any;
type LinkVector = [number, number, number, number, number, InputTypeName];

export type APIWorkflow = {
  config: Record<string, any>;
  extra: WorkflowExtras & Record<string, any>;
  groups: any[];
  last_link_id: number;
  last_node_id: number;
  links: LinkVector[];
  nodes: APIWorkflowNode[];
  version: Float32Array;
};

export type APIWorkflowNode = {
  flags: Record<string, any>;
  id: number;
  mode: number;
  order: number;
  outputs: APIWorkflowNodeOutput[];
  pos: [number, number];
  properties: APIWorkflowNodeProps & Record<string, any>;
  size: [number, number];
  type: str; // class name
  widgets_values: any[];
};

type WorkflowExtras = {
  ds: {
    offset: [number, number];
  };
  scale: float;
};

type APIWorkflowNodeOutput = {
  name: InputTypeName;
  type: InputTypeName;
  links: number[];
  shape: number;
  slot_index: number;
};

type APIWorkflowNodeProps = {
  "Node name for S&R": str;
};
