from dataclasses import dataclass

from fwordle import serializer


@dataclass
class GameParameters(serializer.Simple):
    word_length: int
    max_guesses: int

    @classmethod
    def default(cls) -> "GameParameters":
        return GameParameters(5, 6)
