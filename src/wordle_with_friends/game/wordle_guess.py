import dataclasses
import enum
from typing import List

from src.wordle_with_friends import wtypes, serializer


class WordleLetterState(enum.IntEnum):
    UNKNOWN = enum.auto()
    CORRECT = enum.auto()
    INCORRECT = enum.auto()


@dataclasses.dataclass
class WordleLetterGuess(serializer.Simple):
    letter: str
    player_id: wtypes.PlayerId
    state: WordleLetterState


class WordleGuess(serializer.Simple):
    letters: List[WordleLetterGuess]

    def __init__(self):
        self.letters = []

    def __len__(self):
        return len(self.letters)

    def join(self) -> str:
        return "".join(lg.letter for lg in self.letters)

    def append(self, letter: str, player_id: wtypes.PlayerId):
        self.letters.append(WordleLetterGuess(letter, player_id, WordleLetterState.UNKNOWN))

    def pop(self):
        if len(self.letters) > 0:
            self.letters.pop()
