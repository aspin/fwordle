import * as React from "react";
import Letter from "../letter/Letter";
import { Stack } from "@mui/material";
import { GameGuessLetters, Player } from "../../types/game";

interface WordProps {
  enabled: boolean;
  letters: GameGuessLetters;
  players: Player[]; // TODO: decide on a better way for this
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

    // TODO: improve this call
    const player = props.players.filter(
      (player) => player.id == props.letters[i].playerId,
    );

    let username = "";
    if (player.length == 1) {
      username = player[0].username;
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
