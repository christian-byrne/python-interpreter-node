// Returned by `api.getItems("history")`
export type APIHistory = {
  History: APIHistoryItem[];
};

export type APIOutputText = char[];

export type APIOutputRecord = {
  text: APIOutputText;
} & Record<string, any>;

export type APIHistoryItem = {
  outputs: {
    [id: number]: APIOutputRecord;
  };
  prompt: PromptTuple;
  status: {
    completed: bool;
    message: [
      string,
      {
        prompt_id: string;
      }
    ];
  };
};

type PromptTuple = [
  executionNumber: number,
  clientID: number,
  ...nodes: APINode[]
];

export type APINode = {
  class_type?: str;
  inputs?: Record<string, any>;
  _meta?: Record<string, any>;
  client_id?: number;
  extra_pnginfo?: APIWorkflow;
};

d;
