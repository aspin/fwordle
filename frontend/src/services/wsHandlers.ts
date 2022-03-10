import { AppDispatch } from "../store";
import {
  setConnected,
  setCurrentWord,
  setParams,
  setPlayers,
  submitGuess,
} from "../features/game/gameSlice";
import { GameGuess } from "../types/game";

function handle(dispatch: AppDispatch, data: object) {
  // TODO: should really determine game params vs event better...
  if ("wordLength" in data) {
    handleParams(dispatch, data as ParamsUpdate);
  }

  if ("event" in data) {
    handleEvent(dispatch, data as GameEvent);
  }
}

interface ParamsUpdate {
  wordLength: number;
  maxGuesses: number;
}

function handleParams(dispatch: AppDispatch, data: ParamsUpdate) {
  dispatch(setParams(data));
  dispatch(setConnected(true));
}

interface GameEvent {
  event: string;
  params: unknown;
}

function handleEvent(dispatch: AppDispatch, data: GameEvent) {
  console.log("got a game event", data);

  let guess;
  switch (data.event) {
    case "LETTER_ADDED":
      guess = data.params as GameGuess;
      dispatch(setCurrentWord(guess.letters));
      break;
    case "LETTER_DELETED":
      guess = data.params as GameGuess;
      dispatch(setCurrentWord(guess.letters));
      break;
    case "PLAYER_CHANGED":
      dispatch(setPlayers(data.params as string[]));
      break;
    case "SUBMISSION_RESULT":
      dispatch(submitGuess((data.params as GameGuess).letters));
      break;
  }
}

export { handle };
