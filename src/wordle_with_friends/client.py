import asyncio
import logging

import aiohttp

from src.wordle_with_friends import serializer, models, config

logger = logging.getLogger(__name__)


async def main():
    session_id = await create_session()
    logger.info("connecting to session %s...", session_id)
    await connect_session(session_id)


async def create_session() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9000/new") as response:
            response_json = await response.json()
            session = serializer.decode(models.Session, response_json)
            return session.id


async def connect_session(session_id: str):
    session = aiohttp.ClientSession()
    ws = await session.ws_connect(f"ws://127.0.0.1:9000/session/{session_id}")

    game_parameters = await ws.receive()
    logger.info("session %s parameters: %s", session_id, game_parameters.data)

    msg: aiohttp.WSMessage
    while True:
        await ws.send_json(models.PlayerAction("ping", []), dumps=serializer.dumps)
        msg = await ws.receive()
        logger.info("response from server: %s", msg.data)
        await asyncio.sleep(5)


if __name__ == "__main__":
    config.setup_logger()
    asyncio.get_event_loop().run_until_complete(main())
