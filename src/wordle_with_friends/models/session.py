import uuid
from typing import Any, Dict, List

from src.wordle_with_friends import serializer, wtypes
from src.wordle_with_friends.models.player_action import PlayerAction
from src.wordle_with_friends.models.game_parameters import GameParameters


class Session(serializer.Custom):
    id: wtypes.SessionId
    players: List[wtypes.PlayerId]
    current_parameters: GameParameters

    def __init__(self, session_id: wtypes.SessionId):
        self.id = session_id
        self.players = []
        self.current_parameters = GameParameters.default()

    def add_player(self) -> wtypes.PlayerId:
        player_id = wtypes.PlayerId(uuid.uuid4())
        self.players.append(player_id)
        return player_id

    def remove_player(self, player_id: wtypes.PlayerId) -> bool:
        """
        Removes a player from the session, and indicates if session is empty and should be closed.

        :param player_id: player to remove
        :return: if session is now empty
        """
        self.players.remove(player_id)
        return len(self.players) == 0

    def act(self, player_id: wtypes.PlayerId, action: PlayerAction):
        return

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.id, "players": self.players}

    @classmethod
    def new(cls) -> "Session":
        return Session(wtypes.SessionId(uuid.uuid4()))

    @classmethod
    def from_json(cls, dict_args: Dict[str, Any]) -> "Session":
        session = Session(dict_args["id"])
        session.players = dict_args["players"]
        return session
