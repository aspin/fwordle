from dataclasses import dataclass
from typing import List

from fwordle import serializer, wtypes


@dataclass
class Session(serializer.Simple):
    id: wtypes.SessionId
    players: List[wtypes.PlayerId]

    @classmethod
    def from_impl(cls, session: wtypes.Session) -> "Session":
        return Session(session.id, [player.id for player in session.players])
