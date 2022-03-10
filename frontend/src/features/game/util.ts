import { GameGuessLetters, GameGuessLetterState } from "../../types/game";

const alphabet = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
];

export function letterStates(
  guesses: GameGuessLetters[],
): Map<string, GameGuessLetterState> {
  const map = new Map();
  for (const letter of alphabet) {
    map[letter] = GameGuessLetterState.Unknown;
  }

  for (const guess of guesses) {
    for (const lg of guess) {
      const guessedLetter = lg.letter.toUpperCase();
      if (map[guessedLetter] == GameGuessLetterState.Unknown) {
        // if unknown, always update
        map[guessedLetter] = lg.state;
      } else if (map[guessedLetter] < lg.state) {
        // otherwise, only update if stored state is > that previous
        // this means that CORRECT can not be overridden by PARTIAL or INCORRECT
        map[guessedLetter] = lg.state;
      }
    }
  }

  return map;
}

export function unusedLetters(words: string[]): string[] {
  const remaining = {};
  for (const letter of alphabet) {
    remaining[letter] = 1;
  }

  for (const word of words) {
    for (const letter of word) {
      const normalizedLetter = letter.toUpperCase();
      if (normalizedLetter in remaining) {
        delete remaining[normalizedLetter];
      }

      if (Object.keys(remaining).length == 0) {
        return [];
      }
    }
  }

  return Object.keys(remaining);
}

export function emptyLetters(len: number): string[] {
  return [...Array(len)].map(() => " ");
}

export function splitLetters(s: string): string[] {
  return s.split("");
}

export function lastLetter(s: string): string {
  if (s.length == 0) {
    return "";
  } else {
    return s.charAt(s.length - 1);
  }
}
