import asyncio
import logging
from asyncio import Future
from typing import Dict

from aiohttp import web

from fwordle import wtypes, game, serializer
from fwordle.language import english

logger = logging.getLogger(__name__)


class SessionManager:
    sessions: Dict[wtypes.SessionId, wtypes.Session]

    _closing_timeout_s: int
    _closing_tasks: Dict[wtypes.SessionId, Future]

    def __init__(self, closing_timeout_s: int, dictionary_path: str):
        self.sessions = {}

        logger.info("Loading dictionary of English words...")
        self._dictionary = english.load_length_dict(dictionary_path)
        logger.info("Loaded %s words.", len(self._dictionary))

        self._closing_timeout_s = closing_timeout_s
        self._closing_tasks = {}

    def __contains__(self, item: wtypes.SessionId) -> bool:
        return item in self.sessions

    def create_new(self, encoder: serializer.Encoder) -> wtypes.Session:
        session_id = wtypes.Session.generate_id()
        session = wtypes.Session(
            session_id, game.Wordle(session_id, self._dictionary), encoder
        )
        self.sessions[session.id] = session

        # prepare to timeout session if no one joins in 10x the usual interval
        self._mark_for_close(session.id, 10 * self._closing_timeout_s)

        return session

    async def queue_action(
        self,
        session_id: wtypes.SessionId,
        player_id: wtypes.PlayerId,
        action: wtypes.PlayerAction,
    ):
        await self.sessions[session_id].queue_action(player_id, action)

    def add_player(
        self,
        session_id: wtypes.SessionId,
        username: str,
        ws: web.WebSocketResponse,
    ) -> wtypes.PlayerId:
        self._cancel_session_closing(session_id)
        return self.sessions[session_id].add_player(username, ws)

    def remove_player(
        self, session_id: wtypes.SessionId, player_id: wtypes.PlayerId
    ):
        empty = self.sessions[session_id].remove_player(player_id)
        if empty:
            logger.debug(
                "session %s is now empty: will close in %s seconds if no"
                " further activity",
                session_id,
                self._closing_timeout_s,
            )
            self._mark_for_close(session_id, self._closing_timeout_s)

    def game_parameters(
        self, session_id: wtypes.SessionId
    ) -> wtypes.GameParameters:
        return self.sessions[session_id].current_parameters

    def _mark_for_close(self, session_id: wtypes.SessionId, timeout: int):
        """
        Prepares to close the session if no activity during the timeout.

        In the case that this ends up called multiple times, assume that the
        timeout should be restarted.

        :param session_id: session to close
        """
        self._cancel_session_closing(session_id)
        self._closing_tasks[session_id] = asyncio.create_task(
            self._wait_and_close(session_id, timeout)
        )

    def _cancel_session_closing(self, session_id: wtypes.SessionId):
        previous_task = self._closing_tasks.pop(session_id, None)
        if previous_task is not None:
            previous_task.cancel()

    async def _wait_and_close(self, session_id: wtypes.SessionId, timeout: int):
        await asyncio.sleep(timeout)
        logger.info("session %s is now closed", session_id)
        self.sessions.pop(session_id, None)
