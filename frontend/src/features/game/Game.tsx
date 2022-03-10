import * as React from "react";
import { ChangeEvent, useContext } from "react";
import { useAppSelector } from "../../hooks";
import { Box, Button, Grid, Stack } from "@mui/material";
import Word from "../../components/word/Word";
import { GameWsContext } from "../../services/ws";
import { emptyLetterGuess } from "../../types/game";
import * as _ from "lodash";
import Sidebar from "../../components/sidebar/Sidebar";
import Keyboard from "../../components/keyboard/Keyboard";

interface GameProps {
  sessionId: string;
  disconnect: () => void;
}

export default function Game(props: GameProps) {
  const gameState = useAppSelector((state) => state.game);
  const gameWs = useContext(GameWsContext);

  function disconnect() {
    gameWs.actions.disconnect();
    props.disconnect();
  }

  function row(_value: undefined, i: number) {
    let letters = _.times(gameState.params.wordLength, emptyLetterGuess);
    if (i < gameState.previousGuesses.length) {
      letters = gameState.previousGuesses[i];
    } else if (i == gameState.previousGuesses.length) {
      letters = gameState.currentLetters;
    }

    return (
      <Word
        key={i}
        enabled={gameState.previousGuesses.length == i}
        letters={letters}
        width={gameState.params.wordLength}
        onChange={(letters) => {
          if (letters.length == 0) {
            gameWs.actions.sendDeleteLetter();
          } else if (letters.length == 1) {
            gameWs.actions.sendAddLetter(letters);
          } else {
            console.error(
              "unexpected word change, expected length 0 or 1 but got",
              letters,
            );
          }
        }}
      />
    );
  }

  function submitGuess(e: ChangeEvent<HTMLFormElement>) {
    e.preventDefault();

    if (
      gameState.currentLetters.filter((lg) => lg.letter != " ").length ==
      gameState.params.wordLength
    ) {
      gameWs.actions.submitGuess();
    }
  }

  return (
    <Grid container spacing={4}>
      <Grid item xs={8}>
        <Box component="form" onSubmit={submitGuess} autoComplete="off">
          <Stack spacing={4}>
            <Stack spacing={2}>
              {[...Array(gameState.params.maxGuesses)].map(row)}
            </Stack>
            {/*submit button only to enable Enter submitting*/}
            <Button type="submit" variant="outlined" sx={{ display: "none" }} />
            <Keyboard guesses={gameState.previousGuesses} />
          </Stack>
        </Box>
      </Grid>
      <Grid item xs>
        <Sidebar
          players={gameState.players}
          sessionId={props.sessionId}
          disconnect={disconnect}
        />
      </Grid>
    </Grid>
  );
}
