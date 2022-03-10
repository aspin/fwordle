import asyncio
import logging

import aiohttp

from fwordle import serializer, models, config, wtypes
from fwordle.serializer import Case

logger = logging.getLogger(__name__)


async def main():
    session_id = await create_session()
    # session_id = "5ecf6f84-7482-422e-ba1a-4f37cdb66c29"
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
        logger.info("sending letter to server...")
        await ws.send_json(
            wtypes.PlayerAction("ADD_LETTER", "a"),
            dumps=serializer.encodes(Case.CAMEL),
        )
        await ws.send_json(
            wtypes.PlayerAction("SUBMIT_GUESS", "a"),
            dumps=serializer.encodes(Case.CAMEL),
        )
        msg = await ws.receive()
        logger.info("response from server: %s", msg.data)
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    config.setup_logger()
    asyncio.get_event_loop().run_until_complete(main())
