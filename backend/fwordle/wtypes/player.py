import uuid

from aiohttp import web

from fwordle.wtypes.common import PlayerId


class Player:
    id: PlayerId
    ws: web.WebSocketResponse

    def __init__(self, player_id: PlayerId, ws: web.WebSocketResponse):
        self.id = player_id
        self.ws = ws

    @classmethod
    def new(cls, ws: web.WebSocketResponse) -> "Player":
        return cls(PlayerId(uuid.uuid4()), ws)
