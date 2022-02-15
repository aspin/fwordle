import uuid
from typing import Any, Dict, List

from src.wordle_with_friends import serializer


class Session(serializer.Custom):
    id: str
    players: List[str]

    def __init__(self, session_id: str):
        self.id = session_id
        self.players = []

    def add_player(self) -> str:
        player_id = str(uuid.uuid4())
        self.players.append(player_id)
        return player_id

    def remove_player(self, player_id: str) -> bool:
        """
        Removes a player from the session, and indicates if session is empty and should be closed.

        :param player_id: player to remove
        :return: if session is now empty
        """
        self.players.remove(player_id)
        return len(self.players) == 0

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.id, "players": self.players}

    @classmethod
    def new(cls):
        return Session(str(uuid.uuid4()))
