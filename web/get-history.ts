import { api } from "@comfy-main-web/scripts/api.js";
import { LGraphNodeExtension } from "./types/comfy-app";
import { APIHistory, APIHistoryItem } from "./types/history";

export async function getRecentHistoryItem(
  node: LGraphNodeExtension
): Promise<APIHistoryItem | undefined> {
  return new Promise<APIHistoryItem>((resolve, reject) => {
    api
      .getItems("history")
      .then((history: APIHistory) => {
        const lastExecution: APIHistoryItem =
          history.History[history.History.length - 1];
        if (lastExecution) {
          console.debug("Last execution history item:", lastExecution);
          resolve(lastExecution);
        } else {
          console.debug("No history items found");
          resolve(undefined);
        }
      })
      .catch((error) => {
        console.error("Error trying to get history from API", error);
        reject(new Error(error));
      });
  });
}
