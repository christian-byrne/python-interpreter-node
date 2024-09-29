import { app } from "@comfy-main-web/scripts/app.js";
import { ComfyWidgets } from "@comfy-main-web/scripts/widgets.js";
import { APIOutputRecord } from "./types/history.js";
import { LGraphNodeExtension } from "./types/comfy-app.js";
import { ComfyWidget } from "./types/widgets.js";
import { LGraph } from "@comfy-main-web/types/litegraph.js";
import { nodeConfig } from "./config.js";

export async function appendStdoutWidget(
  node: LGraphNodeExtension,
  liteGraph: LGraph,
  data: APIOutputRecord
) {
  const insertIndex = node.widgets.findIndex(
    (w) => w.name === nodeConfig.stdoutErrId
  );
  if (insertIndex !== -1) {
    console.debug(
      `[onExecuted handler] Removing existing ${nodeConfig.stdoutErrId} widgets after insert index`
    );
    for (let i = insertIndex; i < node.widgets.length; i++) {
      node.widgets[i].onRemove?.();
      liteGraph.setDirtyCanvas(true, true);
    }
    node.widgets.length = insertIndex;
  } else {
    console.debug(
      `[onExecuted handler] No existing ${nodeConfig.stdoutErrId} widgets found. Nothing to remove...`
    );
  }

  const outputWidget: ComfyWidget = ComfyWidgets["STRING"](
    node,
    nodeConfig.stdoutErrId,
    ["STRING", { multiline: true }],
    app
  ).widget;
  outputWidget.value = data.text.join("");
  liteGraph.setDirtyCanvas(true, true);
}
