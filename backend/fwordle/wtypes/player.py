import uuid

from aiohttp import web

from fwordle.wtypes.common import PlayerId


class Player:
    id: PlayerId
    ws: web.WebSocketResponse
    username: str

    def __init__(
        self, player_id: PlayerId, username: str, ws: web.WebSocketResponse
    ):
        self.id = player_id
        self.username = username
        self.ws = ws

    @classmethod
    def new(cls, username: str, ws: web.WebSocketResponse) -> "Player":
        return cls(PlayerId(uuid.uuid4()), username, ws)
