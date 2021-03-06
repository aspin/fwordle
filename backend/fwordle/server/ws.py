import logging

import aiohttp
from aiohttp import web

from fwordle import serializer, config, models, wtypes
from fwordle.server.session import SessionManager

logger = logging.getLogger(__name__)

ALLOW_CORS = {"Access-Control-Allow-Origin": "*"}


class WsServer:
    _app: web.Application
    _config: config.App
    _manager: SessionManager
    _encoder: serializer.Encoder

    def __init__(self, app_config: config.App):
        self._config = app_config
        self._app = web.Application()
        self._app.add_routes(
            [
                web.get("/new", self.handle_new),
                web.get("/session/{session_id}", self.handle_session),
            ]
        )

        self._manager = SessionManager(
            app_config.empty_session_timeout_s, app_config.dictionary_path
        )
        self._encoder = serializer.encodes(app_config.case)

    def run(self):
        web.run_app(self._app, port=9000, print=lambda _: None)

    async def handle_new(self, _request: web.Request) -> web.StreamResponse:
        session = self._manager.create_new(self._encoder)
        logger.debug("creating session %s", session.id)

        return web.json_response(
            models.Session.from_impl(session),
            headers=ALLOW_CORS,
            dumps=self._encoder,
        )

    async def handle_session(self, request: web.Request) -> web.StreamResponse:
        # player must be added and session kept alive before returning control
        # to the event loop to prevent race conditions on session existing
        session_id: str = request.match_info["session_id"]
        if session_id not in self._manager:
            raise web.HTTPNotFound()

        username: str = request.query.get("username", "")
        if username == "":
            raise web.HTTPBadRequest()

        ws = web.WebSocketResponse()

        player_id = self._manager.add_player(session_id, username, ws)
        logger.debug("%s joined session %s", player_id, session_id)

        await ws.prepare(request)
        await ws.send_json(
            self._manager.game_parameters(session_id), dumps=self._encoder
        )

        try:
            msg: aiohttp.WSMessage
            async for msg in ws:
                action = serializer.decodes(
                    wtypes.PlayerAction, msg.data, self._config.case
                )
                await self._manager.queue_action(session_id, player_id, action)
        finally:
            logger.debug("%s has left session %s", player_id, session_id)
            self._manager.remove_player(session_id, player_id)

        return ws


def build(app_config: config.App) -> WsServer:
    return WsServer(app_config)
