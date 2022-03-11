import * as React from "react";
import { ChangeEvent, useState } from "react";
import { Box, Button, Grid, Stack, TextField } from "@mui/material";

interface SessionConnectorProps {
  connect: (sessionId: string, username: string) => void;
  create: (username: string) => void;
  sessionId: string;
}

export default function SessionConnector(props: SessionConnectorProps) {
  const [username, setUsername] = useState<string>("");
  const [isDirty, setIsDirty] = useState<boolean>(false);
  const showError = isDirty && !username;

  function connect(e: ChangeEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsDirty(true);
    if (username) {
      props.connect(e.target["session-id"].value, username);
    }
  }

  function create() {
    setIsDirty(true);
    if (username) {
      props.create(username);
    }
  }

  return (
    <Grid container justifyContent="center" alignItems="center">
      <Grid item xs={3}>
        <Box component="form" onSubmit={connect} autoComplete="off">
          <Stack spacing={2}>
            <TextField
              label="Username"
              id="username"
              error={showError}
              sx={{
                width: "100%",
              }}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              label="Session ID"
              id="session-id"
              defaultValue={props.sessionId}
              sx={{
                width: "100%",
              }}
            />
            <Grid container>
              <Grid item xs={6} sx={{ pr: 1 }}>
                <Button
                  variant="contained"
                  type="submit"
                  sx={{ width: "100%" }}
                >
                  Connect
                </Button>
              </Grid>
              <Grid item xs={6} sx={{ pl: 1 }}>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={create}
                  sx={{ width: "100%" }}
                >
                  Create New
                </Button>
              </Grid>
            </Grid>
          </Stack>
        </Box>
      </Grid>
    </Grid>
  );
}
