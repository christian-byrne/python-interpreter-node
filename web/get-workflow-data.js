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
/**
 * Retrieves the workflow data from the relevant storage API.
 *
 * Note that the comfy api class writes the workflow to `localStorage` always
 * and `sessionStorage` if a client ID is present (sockets).
 *
 * This is done via a 1-second `setInterval`. As a result, the workflow
 * data will not be available until at least 1 second after the workflow is loaded.
 * If this is called at the current time, that shouldn't be a problem. Otherwise set
 * a timeout using the `timeout` parameter.
 *
 * In the case of a socket connection, the client ID is stored in session storage with
 * keyname "clientId". There are indeed scenarios where a clientId is present in
 * sessionStorage and user is not using a socket connection.
 *
 * @param timeout - The timeout in milliseconds to wait for the workflow data to be available.
 * @returns A Promise that resolves to the workflow data if it exists, or null if it doesn't.
 */
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
/**
 * Retrieves the data for specified node in the current workflow data.
 *
 * Note that the ComfyAPI code writes the workflow to the session storage if a client
 * ID is present, and to the local storage otherwise.
 *
 * This is done via a `setInterval` with a 1-second interval. As a result, the workflow
 * data will not be available until at least 1 second after the workflow is loaded.
 *
 * @param id - The ID of the workflow node to retrieve.
 * @returns A Promise that resolves to the APIWorkflowNode with the specified ID, or undefined if not found.
 */
export function getWorkflowNodeById(id) {
    return __awaiter(this, void 0, void 0, function* () {
        const workflow = yield getWorkflowData();
        if (workflow) {
            let ret = workflow.nodes.find((n) => n.id === id);
            if (ret) {
                console.debug(`Workflow data for node ID ${id} found:`, workflow);
            }
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
            if (ret) {
                console.debug(`Workflow data for node name ${name} found:`, workflow);
            }
            return ret;
        }
        return undefined;
    });
}
