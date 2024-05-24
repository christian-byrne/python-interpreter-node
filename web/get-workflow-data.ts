import { api } from "@comfy-main-web/scripts/api.js";
import { APIWorkflow, APIWorkflowNode } from "./types/workflow.js";

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
export async function getWorkflowData(timeout: number = 64): Promise<APIWorkflow | null> {
  return new Promise((resolve) => {
    setTimeout(() => {
      let workflowData: string | null;
      if (api.clientId) {
        workflowData = sessionStorage.getItem(`workflow-${api.clientId}`);
        if (!workflowData) {
          console.warn(
            `No workflow data found in session storage for client ID: ${api.clientId}`
          );
          // Try to fallback to local storage.
          workflowData = localStorage.getItem("workflow");
        }
      } else {
        workflowData = localStorage.getItem("workflow");
      }
      if (workflowData) {
        resolve(JSON.parse(workflowData) as APIWorkflow);
      } else {
        resolve(null);
      }
    }, timeout);
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
export async function getWorkflowNodeById(
  id: number
): Promise<APIWorkflowNode | undefined> {
  const workflow = await getWorkflowData();
  if (workflow) {
    let ret = workflow.nodes.find((n: APIWorkflowNode) => n.id === id);
    if (ret) {
      console.debug(`Workflow data for node ID ${id} found:`, workflow);
    }
    return ret;
  }
  return undefined;
}

export async function getWorkflowNodeByName(
  name: string
): Promise<APIWorkflowNode | undefined> {
  const workflow = await getWorkflowData();
  if (workflow) {
    let ret = workflow.nodes.find((n: APIWorkflowNode) => n.type === name);
    if (ret) {
      console.debug(`Workflow data for node name ${name} found:`, workflow);
    }
    return ret;
  }
  return undefined;
}
