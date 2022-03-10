import * as React from "react";
import { Box, Button, Stack, Typography } from "@mui/material";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import { CopyToClipboard } from "react-copy-to-clipboard";
import PlayerList from "../player_list/PlayerList";

interface SidebarProps {
  players: string[];
  sessionId: string;
  disconnect: () => void;
}

export default function Sidebar(props: SidebarProps) {
  return (
    <Stack spacing={2}>
      <Stack>
        <Box>
          <Typography variant="h4" sx={{ textAlign: "center" }}>
            Game ID
          </Typography>
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            justifyContent="center"
          >
            <Typography variant="body1">{props.sessionId}</Typography>
            <CopyToClipboard text={props.sessionId}>
              <Button sx={{ minWidth: 36 }}>
                <ContentCopyIcon />
              </Button>
            </CopyToClipboard>
          </Stack>
        </Box>
        <Box>
          <Button
            sx={{ mx: "auto", width: 200, display: "block" }}
            onClick={props.disconnect}
          >
            Disconnect
          </Button>
        </Box>
      </Stack>
      <PlayerList players={props.players} />
    </Stack>
  );
}
