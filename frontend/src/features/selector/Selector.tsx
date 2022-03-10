import * as React from "react";
import { useState } from "react";
import { Grid, Typography } from "@mui/material";
import { setSessionId } from "./selectorSlice";
import { useAppDispatch, useAppSelector } from "../../hooks";
import { useNewSessionQuery } from "../../services/session";
import SessionConnector from "../../components/session_connector/SessionConnector";
import GameWsProvider from "../../services/ws";
import Game from "../game/Game";

export default function Selector() {
  // generate indicates if a new session ID should be generated
  const [generate, setGenerate] = useState<boolean>(false);

  // ready indicates if the game is ready to be rendered (e.g. any session ID has been selected)
  const [ready, setReady] = useState<boolean>(false);

  // prefill value if set from generation (but component should not be controlled)
  const selectorState = useAppSelector((state) => state.selector);
  const dispatch = useAppDispatch();

  const sessionId = selectorState.sessionId;

  const skipQuery = !(generate && ready);
  const { data, isLoading } = useNewSessionQuery(undefined, {
    skip: skipQuery,
  });

  if (data) {
    dispatch(setSessionId(data.id));
    setGenerate(false);
  }

  function connectSession(selectedSessionId: string) {
    setReady(true);
    setGenerate(false);
    dispatch(setSessionId(selectedSessionId));
  }

  function createSession() {
    setReady(true);
    setGenerate(true);
  }

  function disconnect() {
    setReady(false);
    setGenerate(false);
  }

  function content() {
    if (isLoading || !ready) {
      return (
        <SessionConnector
          connect={connectSession}
          create={createSession}
          sessionId={sessionId}
        />
      );
    } else {
      return (
        <GameWsProvider sessionId={sessionId}>
          <Game sessionId={sessionId} disconnect={disconnect} />
        </GameWsProvider>
      );
    }
  }

  return (
    <Grid container rowSpacing={4}>
      <Grid item xs={12}>
        <Typography variant="h1" sx={{ textAlign: "center" }}>
          fwordle
        </Typography>
      </Grid>
      <Grid item xs={12}>
        {content()}
      </Grid>
    </Grid>
  );
}
