import * as React from "react";
import { ChangeEvent } from "react";
import { Box, Button, Grid, Stack, TextField } from "@mui/material";

interface SessionConnectorProps {
  connect: (string) => void;
  create: () => void;
  sessionId: string;
}

export default function SessionConnector(props: SessionConnectorProps) {
  function connect(e: ChangeEvent<HTMLFormElement>) {
    e.preventDefault();
    props.connect(e.target["session-id"].value);
  }

  return (
    <Grid container justifyContent="center" alignItems="center">
      <Grid item xs={3}>
        <Box component="form" onSubmit={connect} autoComplete="off">
          <Stack spacing={2}>
            <TextField
              label="Username"
              id="username"
              sx={{
                width: "100%",
              }}
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
                  onClick={props.create}
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
