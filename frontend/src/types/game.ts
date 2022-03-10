import { green, red, yellow } from "@mui/material/colors";

export interface GameParameters {
  maxGuesses: number;
  wordLength: number;
}

export interface Session {
  id: string;
  players: string[];
}

export interface GameGuess {
  letters: GameGuessLetters;
}

export type GameGuessLetters = GameGuessLetter[];

export interface GameGuessLetter {
  letter: string;
  playerId: string;
  state: GameGuessLetterState;
}

export function emptyLetterGuess(): GameGuessLetter {
  return {
    letter: " ",
    playerId: "",
    state: GameGuessLetterState.Unknown,
  };
}

export enum GameGuessLetterState {
  Unknown = 1,
  Correct,
  Partial,
  Incorrect,
}

export const StateColorMapping = {
  [GameGuessLetterState.Correct]: green[800],
  [GameGuessLetterState.Partial]: yellow[500],
  [GameGuessLetterState.Incorrect]: red[700],
};

export function getLetters(gameGuess: GameGuess): string[] {
  return gameGuess.letters.map((lg) => lg.letter);
}
