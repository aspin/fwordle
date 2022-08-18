import enum
from typing import Generic, TypeVar, Dict, Any

from fwordle import serializer

T = TypeVar("T")


class MessageType(enum.Enum):
    HANDSHAKE = enum.auto()
    PING = enum.auto()
    PONG = enum.auto()
    GAME_PARAMETERS = enum.auto()
    GAME_EVENT = enum.auto()
    PLAYER_ACTION = enum.auto()


class Message(serializer.Custom, Generic[T]):
    message_type: MessageType
    payload: T

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_json(self) -> Dict[str, Any]:
        return {
            "message_type": self.message_type,
            "payload": self.payload
        }

    @classmethod
    def from_json(cls, dict_args: Dict[str, Any]) -> "serializer.Custom":
        return cls(dict_args["payload"])
