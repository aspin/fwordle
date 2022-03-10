import uuid

from aiohttp import web

from src.wordle_with_friends.wtypes.common import PlayerId


class Player:
    id: PlayerId
    ws: web.WebSocketResponse

    def __init__(self, player_id: PlayerId, ws: web.WebSocketResponse):
        self.id = player_id
        self.ws = ws

    @classmethod
    def new(cls, ws: web.WebSocketResponse) -> "Player":
        return cls(PlayerId(uuid.uuid4()), ws)
