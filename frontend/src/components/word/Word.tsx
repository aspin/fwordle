import * as React from "react";
import Letter from "../letter/Letter";
import { Stack } from "@mui/material";
import { GameGuessLetters } from "../../types/game";

interface WordProps {
  enabled: boolean;
  letters: GameGuessLetters;
  width: number;
  onChange: (letter: string) => void;
}

export default function Word(props: WordProps) {
  function letter(_value: undefined, i: number) {
    if (!props.letters[i]) {
      debugger;
    }
    // set focus on the first enabled empty spot
    let focus =
      props.enabled &&
      props.letters[i].letter == " " &&
      (i == 0 || props.letters[i - 1].letter != " ");

    // if last letter and is filled (e.g. all letters filled), keep focused
    if (i == props.letters.length - 1 && props.letters[i].letter != " ") {
      focus = props.enabled;
    }

    return (
      <Letter
        key={i}
        enabled={focus}
        guess={props.letters[i]}
        focus={focus}
        onChange={(letter) => props.onChange(letter)}
      />
    );
  }

  return (
    <Stack direction="row" spacing={2}>
      {[...Array(props.width)].map(letter)}
    </Stack>
  );
}
