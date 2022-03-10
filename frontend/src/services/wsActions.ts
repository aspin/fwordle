import * as _ from "lodash";

export interface WsActionsInterface {
  sendAddLetter: (string) => void;
  sendDeleteLetter: () => void;
  submitGuess: () => void;
  disconnect: () => void;
}

function sendAddLetter(ws: WebSocket, letter: string) {
  const event = {
    action: "ADD_LETTER",
    params: letter,
  };
  sendEvent(ws, event);
}

function sendDeleteLetter(ws: WebSocket) {
  const event = {
    action: "DELETE_LETTER",
    params: null,
  };
  sendEvent(ws, event);
}

function submitGuess(ws: WebSocket) {
  const event = {
    action: "SUBMIT_GUESS",
    params: null,
  };
  sendEvent(ws, event);
}

function disconnect(ws: WebSocket) {
  if (!ws) {
    return;
  }

  ws.close();
}

function sendEvent(ws: WebSocket, e: object) {
  // probably a good idea, but not strictly necessary?
  // if (ws.readyState != WebSocket.OPEN) {
  //   return;
  // }
  console.log("submitting event to server", e);
  ws.send(JSON.stringify(e));
}

export function generateActions(ws: WebSocket): WsActionsInterface {
  return {
    sendAddLetter: _.partial(sendAddLetter, ws),
    sendDeleteLetter: _.partial(sendDeleteLetter, ws),
    submitGuess: _.partial(submitGuess, ws),
    disconnect: _.partial(disconnect, ws),
  };
}
