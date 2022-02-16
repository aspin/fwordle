import uuid
from typing import List, Dict, Any

from src.wordle_with_friends.wtypes.game_parameters import GameParameters
from src.wordle_with_friends.wtypes.common import PlayerId, SessionId


class Session:
    id: SessionId
    players: List[PlayerId]
    current_parameters: GameParameters

    def __init__(self, session_id: SessionId):
        self.id = session_id
        self.players = []
        self.current_parameters = GameParameters.default()

    def add_player(self) -> PlayerId:
        player_id = PlayerId(uuid.uuid4())
        self.players.append(player_id)
        return player_id

    def remove_player(self, player_id: PlayerId) -> bool:
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
    def new(cls) -> "Session":
        return Session(SessionId(uuid.uuid4()))

    @classmethod
    def from_json(cls, dict_args: Dict[str, Any]) -> "Session":
        session = Session(dict_args["id"])
        session.players = dict_args["players"]
        return session