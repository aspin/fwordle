from dataclasses import dataclass

from src.wordle_with_friends import serializer, wtypes


@dataclass
class Player(serializer.Simple):
    id: wtypes.PlayerId

    @classmethod
    def from_impl(cls, player: wtypes.Player) -> "Player":
        return Player(player.id)
