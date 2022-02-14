from aiohttp import web


class SocketServer:
    _app: web.Application

    def __init__(self):
        self._app = web.Application()
        self._app.add_routes([
            web.get("/", self.handle_ws)
        ])

    def run(self):
        web.run_app(self._app)

    async def handle_ws(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            await ws.send_str("hello world")


def build() -> SocketServer:
    return SocketServer()
