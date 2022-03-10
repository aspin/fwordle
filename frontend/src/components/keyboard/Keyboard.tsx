import * as React from "react";
import {GameGuessLetters, GameGuessLetterState, StateColorMapping} from "../../types/game";
import { Button, Stack } from "@mui/material";
import { letterStates } from "../../features/game/util";

interface KeyboardProps {
  guesses: GameGuessLetters[];
}

const qwerty = [
  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
  ["Z", "X", "C", "V", "B", "N", "M"],
];

export default function Keyboard(props: KeyboardProps) {
  const ls = letterStates(props.guesses);

  function row(letters: string[], i: number) {
    return (
      <Stack
        key={i}
        spacing={1}
        direction="row"
        alignItems="center"
        justifyContent="center"
      >
        {letters.map(button)}
      </Stack>
    );
  }

  function button(letter: string) {
    let variant: "outlined" | "contained" = "outlined";
    if (ls[letter] != GameGuessLetterState.Unknown) {
      variant = "contained";
    }

    const backgroundColor = StateColorMapping[ls[letter]];

    return (
      <Button
        key={letter}
        variant={variant}
        sx={{
          backgroundColor,
        }}
      >
        {letter}
      </Button>
    );
  }

  return <Stack spacing={1}>{qwerty.map(row)}</Stack>;
}
