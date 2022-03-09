import dataclasses
import enum
from collections import defaultdict
from typing import List

from src.wordle_with_friends import wtypes, serializer


class WordleLetterState(enum.IntEnum):
    UNKNOWN = enum.auto()
    CORRECT = enum.auto()
    PARTIAL = enum.auto()
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

    def verify(self, expected: str):
        if len(expected) != len(self.letters):
            raise ValueError("word was not same length as the guess")

        expected_letters = defaultdict(int)
        for letter in expected:
            expected_letters[letter] += 1

        for i, lg in enumerate(self.letters):
            if lg.letter == expected[i]:
                lg.state = WordleLetterState.CORRECT
                expected_letters[lg.letter] -= 1
            elif expected_letters[lg.letter] > 0:
                # TODO: there's an ordering problem! if partial identified before correct, then there's an issue
                lg.state = WordleLetterState.PARTIAL
                expected_letters[lg.letter] -= 1
            else:
                lg.state = WordleLetterState.INCORRECT
