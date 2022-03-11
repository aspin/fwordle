import * as React from "react";
import {
  Avatar,
  Box,
  Divider,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Typography,
} from "@mui/material";
import ImageIcon from "@mui/icons-material/Image";
import {Player} from "../../types/game";

interface PlayerListProps {
  players: Player[];
}

export default function PlayerList(props: PlayerListProps) {
  function player(_value: Player, i: number) {
    let divider;
    if (i != props.players.length - 1) {
      divider = <Divider />;
    }

    return (
      <React.Fragment key={props.players[i].id}>
        <ListItem>
          <ListItemAvatar>
            <Avatar>
              <ImageIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary={props.players[i].username}
            secondary={props.players[i].id}
          />
        </ListItem>
        {divider}
      </React.Fragment>
    );
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ textAlign: "center" }}>
        Players
      </Typography>
      <List>{props.players.map(player)}</List>
    </Box>
  );
}
