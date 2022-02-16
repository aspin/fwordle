import asyncio
import enum
from typing import Any, Dict, Callable, List, cast

from src.wordle_with_friends import wtypes
from src.wordle_with_friends.wtypes import GameParameters


class WordleAction(enum.Enum):
    ADD_LETTER = enum.auto()
    DELETE_LETTER = enum.auto()
    SUBMIT_GUESS = enum.auto()


class WordleEvent(enum.Enum):
    LETTER_ADDED = enum.auto()
    LETTER_DELETED = enum.auto()
    GUESS_SUBMITTED = enum.auto()


class Wordle(wtypes.Game):
    params: wtypes.GameParameters
    chosen_word: str

    _current_guess: List[str]
    _guesses: List[str]

    _action_map: Dict[WordleAction, Callable[[wtypes.PlayerId, Any], None]]
    _event_queue: "asyncio.Queue[wtypes.BroadcastEvent]"

    def __init__(self):
        self._current_guess = []
        self._guesses = []
        self._event_queue = asyncio.Queue()

        self.set_parameters(wtypes.GameParameters.default())
        self._action_map = {
            WordleAction.ADD_LETTER: self._handle_add,
            WordleAction.DELETE_LETTER: self._handle_delete,
            WordleAction.SUBMIT_GUESS: self._handle_submit,
        }

    def set_parameters(self, game_parameters: GameParameters):
        self.params = game_parameters
        self.chosen_word = self._generate_word()

    def process_action(self, player: wtypes.PlayerId, player_action: wtypes.PlayerAction):
        wordle_action = WordleAction[player_action.action]
        handler = self._action_map[wordle_action]
        handler(player, player_action.params)

    def event_queue(self) -> "asyncio.Queue[wtypes.BroadcastEvent]":
        return self._event_queue

    def _generate_word(self) -> str:
        return "raise"

    def _emit(self, event: WordleEvent, params: Any):
        self._event_queue.put_nowait(wtypes.BroadcastEvent([wtypes.ALL_PLAYER_ID], wtypes.GameEvent(event.name, params)))

    def _handle_add(self, player: wtypes.PlayerId, params: Any):
        letter = cast(str, params)

        # validate current game state TODO: decide if should be ignored?
        if len(letter) > 1 or len(self._current_guess) >= self.params.word_length:
            return

        self._current_guess.append(letter)
        self._emit(WordleEvent.LETTER_ADDED, "".join(self._current_guess))

    def _handle_delete(self, player: wtypes.PlayerId, params: Any):
        if len(self._current_guess) <= 0:
            return

        self._current_guess.pop()
        self._emit(WordleEvent.LETTER_DELETED, "".join(self._current_guess))

    def _handle_submit(self, player: wtypes.PlayerId, params: Any):
        if len(self._current_guess) != self.params.word_length or len(self._guesses) >= self.params.max_attempts:
            return

        self._guesses.append("".join(self._current_guess))
        self._current_guess = []
        self._emit(WordleEvent.GUESS_SUBMITTED, self._guesses)  # TODO: indicate info about which letters were right

