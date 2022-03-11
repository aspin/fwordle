import enum
from collections import defaultdict
from dataclasses import dataclass
from typing import List

from fwordle import wtypes, serializer


class WordleLetterState(enum.IntEnum):
    UNKNOWN = enum.auto()
    CORRECT = enum.auto()
    PARTIAL = enum.auto()
    INCORRECT = enum.auto()


@dataclass
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

    def __repr__(self):
        return f"WordleGuess({self.join()})"

    def __str__(self):
        return repr(self)

    def join(self) -> str:
        return "".join(lg.letter for lg in self.letters)

    def append(self, letter: str, player_id: wtypes.PlayerId):
        self.letters.append(
            WordleLetterGuess(letter, player_id, WordleLetterState.UNKNOWN)
        )

    def pop(self):
        if len(self.letters) > 0:
            self.letters.pop()

    def verify(self, expected: str) -> bool:
        if len(expected) != len(self.letters):
            raise ValueError("word was not same length as the guess")

        # find all expected letters
        expected_letters = defaultdict(int)
        for letter in expected:
            expected_letters[letter] += 1

        # clean up any previous verification
        for lg in self.letters:
            lg.state = WordleLetterState.UNKNOWN

        # first pass: mark all correct letters
        for i, lg in enumerate(self.letters):
            if lg.letter == expected[i]:
                lg.state = WordleLetterState.CORRECT
                expected_letters[lg.letter] -= 1

        # second pass: mark all partial and incorrect letters if not
        # already correct
        for i, lg in enumerate(self.letters):
            if lg.state == WordleLetterState.CORRECT:
                continue

            if expected_letters[lg.letter] > 0:
                lg.state = WordleLetterState.PARTIAL
                expected_letters[lg.letter] -= 1
            else:
                lg.state = WordleLetterState.INCORRECT

        return all(lg.state == WordleLetterState.CORRECT for lg in self.letters)
