import asyncio
import logging
import uuid
from asyncio import Future
from typing import List, Tuple, Mapping, Any, MutableMapping, Optional

from aiohttp import web

from fwordle import serializer
from fwordle.wtypes.common import PlayerId, SessionId, ALL_PLAYER_ID
from fwordle.wtypes.game import PlayerAction, GameEvent, Game
from fwordle.wtypes.game_parameters import GameParameters
from fwordle.wtypes.player import Player

_logger = logging.getLogger(__name__)


class SessionLogAdapter(logging.LoggerAdapter):
    _session_id: SessionId

    def __init__(
        self,
        session_id: SessionId,
        logger: logging.Logger,
        extra: Optional[Mapping[str, object]] = None,
    ):
        if extra is None:
            extra = {}
        super().__init__(logger, extra)
        self._session_id = session_id

    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> Tuple[Any, MutableMapping[str, Any]]:
        return f"[S:{self._session_id}] {msg}", kwargs


class Session:
    id: SessionId
    players: List[Player]
    current_parameters: GameParameters
    game: Game

    _encoder: serializer.Encoder
    _action_task: Future
    _action_queue: "asyncio.Queue[Tuple[PlayerId, PlayerAction]]"

    _event_task: Future
    _log: logging.LoggerAdapter

    def __init__(
        self, session_id: SessionId, game: Game, encoder: serializer.Encoder
    ):
        self.id = session_id
        self.players = []
        self.game = game
        self.current_parameters = GameParameters.default()

        self._encoder = encoder
        self._action_task = asyncio.create_task(self._process_actions())
        self._action_queue = asyncio.Queue()

        self._event_task = asyncio.create_task(self._process_events())
        self._log = SessionLogAdapter(session_id, _logger)

    def add_player(self, username: str, ws: web.WebSocketResponse) -> PlayerId:
        player = Player.new(username, ws)
        self.players.append(player)
        self.game.on_player_added(player)
        return player.id

    def remove_player(self, player_id: PlayerId) -> bool:
        """
        Removes a player from the session, and indicates if session is empty
        and should be closed.

        :param player_id: player to remove
        :return: if session is now empty
        """
        self.players = [
            player for player in self.players if player.id != player_id
        ]
        self.game.on_player_removed(player_id)
        return len(self.players) == 0

    async def queue_action(self, player_id: PlayerId, action: PlayerAction):
        await self._action_queue.put((player_id, action))

    async def broadcast(self, player_ids: List[PlayerId], event: GameEvent):
        broadcast_all = len(player_ids) == 1 and player_ids[0] == ALL_PLAYER_ID
        tasks = []
        for player in self.players:
            if broadcast_all or player.id in player_ids:
                tasks.append(
                    asyncio.create_task(
                        player.ws.send_json(event, dumps=self._encoder)
                    )
                )

        await asyncio.wait(tasks)

    def close(self):
        self._action_task.cancel()
        self._event_task.cancel()

    async def _process_actions(self):
        while True:
            player_id, action = await self._action_queue.get()
            self._log.debug(
                "processing player action: %s => %s", player_id, action
            )
            self.game.process_action(player_id, action)

    async def _process_events(self):
        while True:
            try:
                broadcast = await self.game.event_queue().get()
                self._log.debug("process broadcast: %s", broadcast)
                await self.broadcast(broadcast.players, broadcast.event)
            except asyncio.CancelledError:
                return
            except Exception as e:
                self._log.error(e)

    @classmethod
    def generate_id(cls) -> SessionId:
        return SessionId(uuid.uuid4())
