import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import {
  emptyLetterGuess,
  GameGuessLetters,
  GameParameters,
} from "../../types/game";
import * as _ from "lodash";

export interface GameSlice {
  params: GameParameters;
  currentLetters: GameGuessLetters;
  previousGuesses: GameGuessLetters[];
  players: string[];
  connected: boolean;
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
    setPlayers: (state, action: PayloadAction<string[]>) => {
      state.players = action.payload;
    },
    submitGuess: (state, action: PayloadAction<GameGuessLetters>) => {
      state.previousGuesses.push(action.payload);
      state.currentLetters = _.times(state.params.wordLength, emptyLetterGuess);
    },
  },
});

export const {
  setConnected,
  setParams,
  setCurrentWord,
  setPlayers,
  submitGuess,
} = gameSlice.actions;

export default gameSlice.reducer;
