import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple, List

from src.wordle_with_friends import serializer
from src.wordle_with_friends.wtypes.common import PlayerId


@dataclass
class PlayerAction(serializer.Simple):
    action: str
    params: Any


@dataclass
class GameEvent(serializer.Simple):
    event: str
    params: Any


class BroadcastEvent(NamedTuple):
    players: List[PlayerId]  # empty for all
    event: GameEvent


class Game(ABC):
    @abstractmethod
    def process_action(self, player: PlayerId, action: PlayerAction):
        pass

    @abstractmethod
    def event_queue(self) -> "asyncio.Queue[BroadcastEvent]":
        pass
