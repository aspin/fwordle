import asyncio

from src.wordle_with_friends import wtypes
from src.wordle_with_friends.wtypes.game import Game


class Wordle(Game):
    def process_action(self, player: wtypes.PlayerId, action: wtypes.PlayerAction):
        pass

    def event_queue(self) -> "asyncio.Queue[wtypes.BroadcastEvent]":
        pass

