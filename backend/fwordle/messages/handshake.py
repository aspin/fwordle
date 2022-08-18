from dataclasses import dataclass

from fwordle import serializer
from fwordle.messages.base import Message, MessageType


@dataclass
class HandshakePayload(serializer.Simple):
    session_id: str
    username: str



class Handshake(Message):
    def __init__(self):
        self.message_type = MessageType.HANDSHAKE
