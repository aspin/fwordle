import asyncio
import logging
import uuid
from asyncio import Future
from typing import List, Tuple

from aiohttp import web

from src.wordle_with_friends import serializer
from src.wordle_with_friends.wtypes.common import PlayerId, SessionId, ALL_PLAYER_ID
from src.wordle_with_friends.wtypes.game_parameters import GameParameters
from src.wordle_with_friends.wtypes.player import Player
from src.wordle_with_friends.wtypes.game import PlayerAction, GameEvent, Game


logger = logging.getLogger(__name__)


class Session:
    id: SessionId
    players: List[Player]
    current_parameters: GameParameters
    game: Game

    _encoder: serializer.Encoder
    _action_task: Future
    _action_queue: "asyncio.Queue[Tuple[PlayerId, PlayerAction]]"

    _event_task: Future

    def __init__(self, session_id: SessionId, game: Game, encoder: serializer.Encoder):
        self.id = session_id
        self.players = []
        self.game = game
        self.current_parameters = GameParameters.default()

        self._encoder = encoder
        self._action_task = asyncio.create_task(self._process_actions())
        self._action_queue = asyncio.Queue()

        self._event_task = asyncio.create_task(self._process_events())

    def add_player(self, ws: web.WebSocketResponse) -> PlayerId:
        player = Player.new(ws)
        self.players.append(player)
        self.game.on_player_added(player.id)
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

    async def broadcast(self, player_ids: List[PlayerId], event: GameEvent):
        broadcast_all = len(player_ids) == 1 and player_ids[0] == ALL_PLAYER_ID
        tasks = []
        for player in self.players:
            if broadcast_all or player.id in player_ids:
                tasks.append(
                    asyncio.create_task(player.ws.send_json(event, dumps=self._encoder))
                )

        await asyncio.wait(tasks)

    def close(self):
        self._action_task.cancel()
        self._event_task.cancel()

    async def _process_actions(self):
        while True:
            player_id, action = await self._action_queue.get()
            logger.debug("[S:%s][P:%s] processing action: %s", self.id, player_id, action)
            self.game.process_action(player_id, action)

    async def _process_events(self):
        while True:
            try:
                broadcast = await self.game.event_queue().get()
                logger.debug("[S:%s] processing broadcast: %s", self.id, broadcast)
                await self.broadcast(broadcast.players, broadcast.event)
            except Exception as e:
                logger.error(e)

    @classmethod
    def new(cls, game: Game, encoder: serializer.Encoder) -> "Session":
        return Session(SessionId(uuid.uuid4()), game, encoder)
