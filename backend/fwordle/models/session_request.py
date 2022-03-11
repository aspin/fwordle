from dataclasses import dataclass

from fwordle import serializer, wtypes


@dataclass
class SessionRequest(serializer.Simple):
    id: wtypes.SessionId
    username: str
