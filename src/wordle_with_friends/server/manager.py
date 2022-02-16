import asyncio
import logging
from asyncio import Future
from typing import Dict

from aiohttp import web

from src.wordle_with_friends import wtypes, game

logger = logging.getLogger(__name__)


class SessionManager:
    sessions: Dict[wtypes.SessionId, wtypes.Session]

    _closing_timeout_s: int
    _closing_tasks: Dict[wtypes.SessionId, Future]

    def __init__(self, closing_timeout_s: int):
        self.sessions = {}
        self._closing_timeout_s = closing_timeout_s
        self._closing_tasks = {}

    def __contains__(self, item: wtypes.SessionId) -> bool:
        return item in self.sessions

    def create_new(self) -> wtypes.Session:
        session = wtypes.Session.new(game.Wordle())
        self.sessions[session.id] = session

        # TODO: prepare a timeout if session is never used
        return session

    async def queue_action(
        self, session_id: wtypes.SessionId, player_id: wtypes.PlayerId, action: wtypes.PlayerAction
    ):
        await self.sessions[session_id].queue_action(player_id, action)

    def add_player(
        self, session_id: wtypes.SessionId, ws: web.WebSocketResponse
    ) -> wtypes.PlayerId:
        self._cancel_session_closing(session_id)
        return self.sessions[session_id].add_player(ws)

    def remove_player(self, session_id: wtypes.SessionId, player_id: wtypes.PlayerId):
        empty = self.sessions[session_id].remove_player(player_id)
        if empty:
            self._mark_for_close(session_id)

    def game_parameters(self, session_id: wtypes.SessionId) -> wtypes.GameParameters:
        return self.sessions[session_id].current_parameters

    def _mark_for_close(self, session_id: wtypes.SessionId):
        """
        Prepares to close the session if no activity during the timeout.

        In the case that this ends up called multiple times, assume that the timeout should be
        restarted.

        :param session_id: session to close
        """
        logger.debug(
            "session %s is now empty: will close in %s seconds if no further activity",
            session_id,
            self._closing_timeout_s,
        )
        self._cancel_session_closing(session_id)
        self._closing_tasks[session_id] = asyncio.create_task(
            self._wait_and_close(session_id, self._closing_timeout_s)
        )

    def _cancel_session_closing(self, session_id: wtypes.SessionId):
        previous_task = self._closing_tasks.pop(session_id, None)
        if previous_task is not None:
            previous_task.cancel()

    async def _wait_and_close(self, session_id: wtypes.SessionId, timeout: int):
        await asyncio.sleep(timeout)
        logger.debug("session %s is now closed", session_id)
        self.sessions.pop(session_id, None)
