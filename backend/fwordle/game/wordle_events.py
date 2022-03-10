import enum


class WordleAction(enum.Enum):
    ADD_LETTER = enum.auto()
    DELETE_LETTER = enum.auto()
    SUBMIT_GUESS = enum.auto()


class WordleEvent(enum.Enum):
    LETTER_ADDED = enum.auto()
    LETTER_DELETED = enum.auto()
    SUBMISSION_NOT_A_WORD = enum.auto()
    SUBMISSION_RESULT = enum.auto()
    PLAYER_CHANGED = enum.auto()


