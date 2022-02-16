from dataclasses import dataclass

from src.wordle_with_friends import serializer


@dataclass
class GameParameters(serializer.Simple):
    word_length: int
    max_attempts: int

    @classmethod
    def default(cls) -> "GameParameters":
        return GameParameters(5, 6)
