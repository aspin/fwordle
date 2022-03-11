import * as React from "react";
import Letter from "../letter/Letter";
import { Stack } from "@mui/material";
import { GameGuessLetters, Player } from "../../types/game";

interface WordProps {
  enabled: boolean;
  letters: GameGuessLetters;
  players: Map<string, Player>;
  width: number;
  onChange: (letter: string) => void;
}

export default function Word(props: WordProps) {
  function letter(_value: undefined, i: number) {
    const lg = props.letters[i];

    // set focus on the first enabled empty spot
    let focus =
      props.enabled &&
      lg.letter == " " &&
      (i == 0 || props.letters[i - 1].letter != " ");

    // if last letter and is filled (e.g. all letters filled), keep focused
    if (i == props.letters.length - 1 && lg.letter != " ") {
      focus = props.enabled;
    }

    const player = props.players[lg.playerId];
    let username = "";
    if (player) {
      username = player.username;
    }

    return (
      <Letter
        key={i}
        enabled={focus}
        guess={props.letters[i]}
        username={username}
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
