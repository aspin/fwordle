import * as React from "react";
import { ChangeEvent, useEffect } from "react";
import { TextField } from "@mui/material";
import { lastLetter } from "../../features/game/util";
import { GameGuessLetter, StateColorMapping } from "../../types/game";

interface LetterProps {
  guess: GameGuessLetter;
  enabled: boolean;
  focus: boolean;
  onChange: (str) => void;
}

export default function Letter(props: LetterProps) {
  function onChange(e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) {
    props.onChange(lastLetter(e.target.value));
  }

  const borderColor = StateColorMapping[props.guess.state];

  let inputRef;
  const tf = (
    <TextField
      label={props.guess.playerId}
      value={props.guess.letter.toUpperCase()}
      disabled={!props.enabled}
      inputRef={(e) => (inputRef = e)}
      onChange={onChange}
      sx={{
        "& .MuiOutlinedInput-root.Mui-disabled": {
          "& fieldset": {
            borderColor,
            borderWidth: 2,
          },
        },
      }}
    />
  );

  // force element to be focused if it's the next available
  useEffect(() => {
    if (props.focus) {
      inputRef.focus();
    }
  });

  return tf;
}
