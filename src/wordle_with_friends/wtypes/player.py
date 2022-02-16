from aiohttp import web

from src.wordle_with_friends import serializer, wtypes
from src.wordle_with_friends.wtypes.common import PlayerId


class Player(serializer.Custom):
    id: wtypes.PlayerId
    ws: web.WebSocketResponse

    def __init__(self, player_id: PlayerId, ws: web.WebSocketResponse):
        self.id = player_id
        self.ws = ws
