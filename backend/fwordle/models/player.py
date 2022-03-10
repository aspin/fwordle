from dataclasses import dataclass

from fwordle import serializer, wtypes


@dataclass
class Player(serializer.Simple):
    id: wtypes.PlayerId

    @classmethod
    def from_impl(cls, player: wtypes.Player) -> "Player":
        return Player(player.id)
