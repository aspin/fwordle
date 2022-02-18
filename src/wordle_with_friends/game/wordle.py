import asyncio
import enum
import logging
from typing import Any, Dict, Callable, List, cast

from src.wordle_with_friends import wtypes
from src.wordle_with_friends.wtypes import GameParameters, PlayerId

logger = logging.getLogger(__name__)


class WordleAction(enum.Enum):
    ADD_LETTER = enum.auto()
    DELETE_LETTER = enum.auto()
    SUBMIT_GUESS = enum.auto()


class WordleEvent(enum.Enum):
    LETTER_ADDED = enum.auto()
    LETTER_DELETED = enum.auto()
    SUBMISSION_NOT_A_WORD = enum.auto()
    SUBMISSION_RESULT = enum.auto()
    PLAYER_JOINED = enum.auto()


class Wordle(wtypes.Game):
    params: wtypes.GameParameters
    chosen_word: str

    _current_guess: List[str]
    _guesses: List[str]

    _action_map: Dict[WordleAction, Callable[[wtypes.PlayerId, Any], None]]
    _event_queue: "asyncio.Queue[wtypes.BroadcastEvent]"
    _players: List[PlayerId]

    def __init__(self):
        self._current_guess = []
        self._guesses = []
        self._event_queue = asyncio.Queue()
        self._players = []

        self.set_parameters(wtypes.GameParameters.default())
        self._action_map = {
            WordleAction.ADD_LETTER: self._handle_add,
            WordleAction.DELETE_LETTER: self._handle_delete,
            WordleAction.SUBMIT_GUESS: self._handle_submit,
        }

    def on_player_added(self, player_id: PlayerId):
        self._players.append(player_id)

        self._emit(player_id, WordleEvent.LETTER_ADDED, "".join(self._current_guess))
        self._emit_all(WordleEvent.PLAYER_JOINED, self._players)

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

    def _emit(self, player_id: PlayerId, event: WordleEvent, params: Any):
        logger.debug("emitting event %s to player %s", event, player_id)
        self._event_queue.put_nowait(
            wtypes.BroadcastEvent([player_id], wtypes.GameEvent(event.name, params),)
        )

    def _emit_all(self, event: WordleEvent, params: Any):
        logger.debug("emitting event %s", event)
        self._event_queue.put_nowait(
            wtypes.BroadcastEvent([wtypes.ALL_PLAYER_ID], wtypes.GameEvent(event.name, params))
        )

    def _handle_add(self, player: wtypes.PlayerId, params: Any):
        letter = cast(str, params)

        # validate input + current game state
        if (
            len(letter) > 1
            or len(self._current_guess) >= self.params.word_length
            or not letter.isalpha()
        ):
            return

        self._current_guess.append(letter)
        self._emit_all(WordleEvent.LETTER_ADDED, "".join(self._current_guess))

    def _handle_delete(self, player: wtypes.PlayerId, params: Any):
        if len(self._current_guess) <= 0:
            return

        self._current_guess.pop()
        self._emit_all(WordleEvent.LETTER_DELETED, "".join(self._current_guess))

    def _handle_submit(self, player: wtypes.PlayerId, params: Any):
        if (
            len(self._current_guess) != self.params.word_length
            or len(self._guesses) >= self.params.max_guesses
        ):
            return

        last_guess = "".join(self._current_guess)
        self._guesses.append(last_guess)
        self._current_guess = []
        self._emit_all(
            WordleEvent.SUBMISSION_RESULT, last_guess
        )  # TODO: indicate info about which letters were right
