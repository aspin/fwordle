from dataclasses import dataclass
from typing import Any

from src.wordle_with_friends import serializer


@dataclass
class PlayerAction(serializer.Simple):
    action: str
    params: Any


@dataclass
class GameEvent(serializer.Simple):
    event: str
    params: Any
