import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple, List

from fwordle import serializer
from fwordle.wtypes.player import Player
from fwordle.wtypes.common import PlayerId
from fwordle.wtypes.game_parameters import GameParameters


@dataclass
class PlayerAction(serializer.Simple):
    action: str
    params: Any


@dataclass
class GameEvent(serializer.Simple):
    event: str
    params: Any


class BroadcastEvent(NamedTuple):
    players: List[PlayerId]  # empty for "all" broadcast
    event: GameEvent


class Game(ABC):
    @abstractmethod
    def on_player_added(self, player: Player):
        pass

    @abstractmethod
    def on_player_removed(self, player_id: PlayerId):
        pass

    @abstractmethod
    def set_parameters(self, game_parameters: GameParameters):
        pass

    @abstractmethod
    def process_action(self, player: PlayerId, player_action: PlayerAction):
        pass

    @abstractmethod
    def event_queue(self) -> "asyncio.Queue[BroadcastEvent]":
        pass
