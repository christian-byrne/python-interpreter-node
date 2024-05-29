var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { api } from "../../scripts/api.js";
export function getWorkflowData() {
    return __awaiter(this, arguments, void 0, function* (timeout = 64) {
        return new Promise((resolve) => {
            setTimeout(() => {
                let workflowData;
                if (api.clientId) {
                    workflowData = sessionStorage.getItem(`workflow-${api.clientId}`);
                    if (!workflowData) {
                        console.warn(`No workflow data found in session storage for client ID: ${api.clientId}`);
                        // Try to fallback to local storage.
                        workflowData = localStorage.getItem("workflow");
                    }
                }
                else {
                    workflowData = localStorage.getItem("workflow");
                }
                if (workflowData) {
                    resolve(JSON.parse(workflowData));
                }
                else {
                    resolve(null);
                }
            }, timeout);
        });
    });
}
export function getWorkflowNodeById(id) {
    return __awaiter(this, void 0, void 0, function* () {
        const workflow = yield getWorkflowData();
        if (workflow) {
            let ret = workflow.nodes.find((n) => n.id === id);
            return ret;
        }
        return undefined;
    });
}
export function getWorkflowNodeByName(name) {
    return __awaiter(this, void 0, void 0, function* () {
        const workflow = yield getWorkflowData();
        if (workflow) {
            let ret = workflow.nodes.find((n) => n.type === name);
            return ret;
        }
        return undefined;
    });
}
