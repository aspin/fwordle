from aiohttp import web


class WsServer:
    _app: web.Application

    def __init__(self):
        self._app = web.Application()
        self._app.add_routes([
            web.get("/", self.handle_ws)
        ])

    def run(self):
        web.run_app(self._app, port=9000)

    async def handle_ws(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        print("got new connection!")

        async for msg in ws:
            print(f"got message: {msg}")
            await ws.send_str("hello world")


def build() -> WsServer:
    return WsServer()
