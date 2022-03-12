import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import {
  correctGuess,
  emptyLetterGuess,
  GameGuessLetters,
  GameGuessLetterState,
  GameParameters,
  Player,
} from "../../types/game";
import * as _ from "lodash";

export interface GameSlice {
  params: GameParameters;
  currentLetters: GameGuessLetters;
  previousGuesses: GameGuessLetters[];
  players: Player[];
  connected: boolean;
  done: boolean;
  victory: boolean;
}

export interface GameGuessAction {
  index: number;
  letter: string;
}

const initialState: GameSlice = {
  params: {
    maxGuesses: 5,
    wordLength: 5,
  },
  currentLetters: _.times(5, emptyLetterGuess),
  previousGuesses: [],
  players: [],
  connected: false,
  done: false,
  victory: false,
};

export const gameSlice = createSlice({
  name: "game",
  initialState,
  reducers: {
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.connected = action.payload;
    },
    setParams: (state, action: PayloadAction<GameParameters>) => {
      state.params = action.payload;
      state.currentLetters = _.times(state.params.wordLength, emptyLetterGuess);
    },
    setCurrentWord: (state, action: PayloadAction<GameGuessLetters>) => {
      for (let i = 0; i < state.currentLetters.length; i++) {
        if (i >= action.payload.length) {
          state.currentLetters[i] = emptyLetterGuess();
        } else {
          state.currentLetters[i] = action.payload[i];
        }
      }
    },
    setPlayers: (state, action: PayloadAction<Player[]>) => {
      state.players = action.payload;
    },
    submitGuess: (state, action: PayloadAction<GameGuessLetters>) => {
      state.previousGuesses.push(action.payload);
      state.currentLetters = _.times(state.params.wordLength, emptyLetterGuess);

      if (correctGuess(action.payload)) {
        state.victory = true;
        state.done = true;
      } else if (state.previousGuesses.length == state.params.maxGuesses) {
        state.done = true;
      }
    },
    setBadGuess: (state, action: PayloadAction<number>) => {
      if (action.payload != state.previousGuesses.length + 1) {
        console.error(
          "received info about unexpected guess: ",
          action.payload,
          " vs ",
          state.previousGuesses.length + 1,
        );
        return;
      }
      state.currentLetters.forEach(
        (lg) => (lg.state = GameGuessLetterState.Incorrect),
      );
    },
  },
});

export const {
  setConnected,
  setParams,
  setCurrentWord,
  setPlayers,
  setBadGuess,
  submitGuess,
} = gameSlice.actions;

export default gameSlice.reducer;
