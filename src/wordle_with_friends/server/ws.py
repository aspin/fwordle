import logging

from aiohttp import web

from src.wordle_with_friends import serializer
from src.wordle_with_friends.server.manager import SessionManager

logger = logging.getLogger(__name__)


class WsServer:
    _app: web.Application
    _manager: SessionManager

    def __init__(self):
        self._app = web.Application()
        self._app.add_routes([
            web.get("/create", self.handle_create),
            web.get("/session/{session_id}", self.handle_session)
        ])

        self._manager = SessionManager()

    def run(self):
        web.run_app(self._app, port=9000)

    async def handle_create(self, _request: web.Request) -> web.StreamResponse:
        session = self._manager.create_new()
        logger.debug("creating session %s", session.id)
        return web.json_response(session, dumps=serializer.dumps)

    async def handle_session(self, request: web.Request) -> web.StreamResponse:
        session_id: str = request.match_info["session_id"]
        if session_id not in self._manager:
            raise web.HTTPNotFound()

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        logger.debug("someone joined session %s", session_id)

        async for msg in ws:
            logger.debug("received message %s", msg)
            await ws.send_str("pong")

        return ws


def build() -> WsServer:
    return WsServer()
