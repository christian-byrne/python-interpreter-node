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
export function getRecentHistoryItem(node) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve, reject) => {
            api
                .getItems("history")
                .then((history) => {
                const lastExecution = history.History[history.History.length - 1];
                if (lastExecution) {
                    console.debug("Last execution history item:", lastExecution);
                    resolve(lastExecution);
                }
                else {
                    console.debug("No history items found");
                    resolve(undefined);
                }
            })
                .catch((error) => {
                console.error("Error trying to get history from API", error);
                reject(new Error(error));
            });
        });
    });
}
