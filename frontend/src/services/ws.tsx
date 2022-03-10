import * as React from "react";
import { useAppDispatch } from "../hooks";
import { handle } from "./wsHandlers";
import { generateActions, WsActionsInterface } from "./wsActions";
import { setConnected } from "../features/game/gameSlice";

let ws;
const wsPath = "ws://localhost:9000";

interface GameWsContextInterface {
  ws: WebSocket;
  actions: WsActionsInterface;
}

export const GameWsContext = React.createContext<GameWsContextInterface>(null);

interface GameWsProps {
  children?: unknown;
  sessionId: string;
}

export default function GameWsProvider(props: GameWsProps) {
  const dispatch = useAppDispatch();

  if (!ws) {
    ws = new WebSocket(`${wsPath}/session/${props.sessionId}`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handle(dispatch, data);
    };
    ws.onclose = () => {
      dispatch(setConnected(false));
    };
  }

  const gameWs: GameWsContextInterface = {
    ws,
    actions: generateActions(ws),
  };

  return (
    <GameWsContext.Provider value={gameWs}>
      {props.children}
    </GameWsContext.Provider>
  );
}
