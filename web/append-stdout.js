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
import { ComfyWidgets } from "../../scripts/widgets.js";
import { nodeConfig } from "./config.js";
export function appendStdoutWidget(node, liteGraph, data) {
    return __awaiter(this, void 0, void 0, function* () {
        var _a, _b;
        const insertIndex = node.widgets.findIndex((w) => w.name === nodeConfig.stdoutErrId);
        if (insertIndex !== -1) {
            console.debug(`[onExecuted handler] Removing existing ${nodeConfig.stdoutErrId} widgets after insert index`);
            for (let i = insertIndex; i < node.widgets.length; i++) {
                (_b = (_a = node.widgets[i]).onRemove) === null || _b === void 0 ? void 0 : _b.call(_a);
                liteGraph.setDirtyCanvas(true, true);
            }
            node.widgets.length = insertIndex;
        }
        else {
            console.debug(`[onExecuted handler] No existing ${nodeConfig.stdoutErrId} widgets found. Nothing to remove...`);
        }
        const outputWidget = ComfyWidgets["STRING"](node, nodeConfig.stdoutErrId, ["STRING", { multiline: true }], app).widget;
        outputWidget.value = data.text.join("");
        liteGraph.setDirtyCanvas(true, true);
    });
}
