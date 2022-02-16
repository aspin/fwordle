import asyncio
import uuid
from asyncio import Future
from typing import List, Tuple

from aiohttp import web

from src.wordle_with_friends import serializer
from src.wordle_with_friends.wtypes.common import PlayerId, SessionId
from src.wordle_with_friends.wtypes.game_parameters import GameParameters
from src.wordle_with_friends.wtypes.player import Player
from src.wordle_with_friends.wtypes.events import PlayerAction, GameEvent


class Session:
    id: SessionId
    players: List[Player]
    current_parameters: GameParameters

    _task: Future
    _action_queue: "asyncio.Queue[Tuple[PlayerId, PlayerAction]]"

    def __init__(self, session_id: SessionId):
        self.id = session_id
        self.players = []
        self.current_parameters = GameParameters.default()

        self._task = asyncio.create_task(self._process_actions())
        self._action_queue = asyncio.Queue()

    def add_player(self, ws: web.WebSocketResponse) -> PlayerId:
        player = Player.new(ws)
        self.players.append(player)
        return player.id

    def remove_player(self, player_id: PlayerId) -> bool:
        """
        Removes a player from the session, and indicates if session is empty and should be closed.

        :param player_id: player to remove
        :return: if session is now empty
        """
        self.players = [player for player in self.players if player.id != player_id]
        return len(self.players) == 0

    async def queue_action(self, player_id: PlayerId, action: PlayerAction):
        await self._action_queue.put((player_id, action))

    async def broadcast(self, event: GameEvent):
        tasks = []
        for player in self.players:
            tasks.append(asyncio.create_task(player.ws.send_json(event, dumps=serializer.dumps)))

        await asyncio.wait(tasks)

    def close(self):
        self._task.cancel()

    async def _process_actions(self):
        while True:
            player_id, action = await self._action_queue.get()
            await self.broadcast(GameEvent("player_took_action", action.action))

    @classmethod
    def new(cls) -> "Session":
        return Session(SessionId(uuid.uuid4()))
