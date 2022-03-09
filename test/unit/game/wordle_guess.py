from typing import List

import pytest

from src.wordle_with_friends.game.wordle_guess import WordleGuess, WordleLetterState


@pytest.fixture
def word_guess() -> WordleGuess:
    wg = WordleGuess()
    wg.append("a", "p1")
    wg.append("r", "p1")
    wg.append("i", "p1")
    wg.append("s", "p1")
    wg.append("e", "p1")
    return wg


@pytest.fixture
def word_guess_multi_letter() -> WordleGuess:
    wg = WordleGuess()
    wg.append("g", "p1")
    wg.append("r", "p1")
    wg.append("e", "p1")
    wg.append("e", "p1")
    wg.append("t", "p1")
    return wg


def verify_word(word_guess: WordleGuess, states: List[WordleLetterState]):
    if len(word_guess.letters) != len(states):
        raise AssertionError("test case was not written correctly")

    for i, lg in enumerate(word_guess.letters):
        assert lg.state == states[i]


def test_wordle_guess_verify_simple(word_guess: WordleGuess):
    assert word_guess.verify("arise")

    assert not word_guess.verify("raise")
    verify_word(
        word_guess,
        [
            WordleLetterState.PARTIAL,
            WordleLetterState.PARTIAL,
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
        ],
    )

    assert not word_guess.verify("ccccc")
    verify_word(
        word_guess,
        [
            WordleLetterState.INCORRECT,
            WordleLetterState.INCORRECT,
            WordleLetterState.INCORRECT,
            WordleLetterState.INCORRECT,
            WordleLetterState.INCORRECT,
        ],
    )


def test_wordle_guess_verify_double_letters(word_guess_multi_letter):
    assert not word_guess_multi_letter.verify("eeeer")
    verify_word(
        word_guess_multi_letter,
        [
            WordleLetterState.INCORRECT,
            WordleLetterState.PARTIAL,
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
            WordleLetterState.INCORRECT,
        ],
    )

    assert not word_guess_multi_letter.verify("grtee")
    verify_word(
        word_guess_multi_letter,
        [
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
            WordleLetterState.PARTIAL,
            WordleLetterState.CORRECT,
            WordleLetterState.PARTIAL,
        ],
    )

    assert not word_guess_multi_letter.verify("grtet")
    verify_word(
        word_guess_multi_letter,
        [
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
            WordleLetterState.INCORRECT,
            WordleLetterState.CORRECT,
            WordleLetterState.CORRECT,
        ],
    )
