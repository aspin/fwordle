import asyncio
import logging
from typing import Any, Dict, Callable, List, cast, MutableMapping, Tuple, Optional, Mapping

from src.wordle_with_friends import wtypes
from src.wordle_with_friends.game.wordle_events import WordleAction, WordleEvent
from src.wordle_with_friends.game.wordle_guess import WordleGuess

_logger = logging.getLogger(__name__)


class Wordle(wtypes.Game):
    params: wtypes.GameParameters
    chosen_word: str

    _session_id: wtypes.SessionId
    _current_guess: WordleGuess
    _guesses: List[WordleGuess]

    _action_map: Dict[WordleAction, Callable[[wtypes.PlayerId, Any], None]]
    _event_queue: "asyncio.Queue[wtypes.BroadcastEvent]"
    _players: List[wtypes.PlayerId]

    class _LogAdapter(logging.LoggerAdapter):
        _wordle: "Wordle"

        def __init__(
            self,
            wordle: "Wordle",
            logger: logging.Logger,
            extra: Optional[Mapping[str, object]] = None,
        ):
            if extra is None:
                extra = {}
            super().__init__(logger, extra)
            self._wordle = wordle

        def process(
            self, msg: Any, kwargs: MutableMapping[str, Any]
        ) -> Tuple[Any, MutableMapping[str, Any]]:
            return f"[S:{self._wordle._session_id}]{self.generate_debug()} {msg}", kwargs

        def generate_debug(self) -> str:
            if self.logger.isEnabledFor(logging.DEBUG):
                last_guess = ""
                if len(self._wordle._guesses) > 0:
                    last_guess = self._wordle._guesses[-1]
                return f"[word: {self._wordle.chosen_word}, last guess: {last_guess}]"
            return ""

    def __init__(self, session_id: str):
        self._session_id = session_id
        self._current_guess = WordleGuess()
        self._guesses = []
        self._event_queue = asyncio.Queue()
        self._players = []
        self._log = Wordle._LogAdapter(self, _logger)

        self.set_parameters(wtypes.GameParameters.default())
        self._action_map = {
            WordleAction.ADD_LETTER: self._handle_add,
            WordleAction.DELETE_LETTER: self._handle_delete,
            WordleAction.SUBMIT_GUESS: self._handle_submit,
        }

    def on_player_added(self, player_id: wtypes.PlayerId):
        self._players.append(player_id)

        self._emit(player_id, WordleEvent.LETTER_ADDED, self._current_guess)
        self._emit_all(WordleEvent.PLAYER_JOINED, self._players)

    def set_parameters(self, game_parameters: wtypes.GameParameters):
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

    def _emit(self, player_id: wtypes.PlayerId, event: WordleEvent, params: Any):
        self._log.debug("emitting event %s to player %s", event, player_id)
        self._event_queue.put_nowait(
            wtypes.BroadcastEvent([player_id], wtypes.GameEvent(event.name, params),)
        )

    def _emit_all(self, event: WordleEvent, params: Any):
        self._log.debug("emitting event %s", event)
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

        self._current_guess.append(letter, player)
        self._emit_all(WordleEvent.LETTER_ADDED, self._current_guess)

    def _handle_delete(self, player: wtypes.PlayerId, params: Any):
        self._current_guess.pop()
        self._emit_all(WordleEvent.LETTER_DELETED, self._current_guess)

    def _handle_submit(self, player: wtypes.PlayerId, params: Any):
        if (
            len(self._current_guess) != self.params.word_length
            or len(self._guesses) >= self.params.max_guesses
        ):
            return

        last_guess = self._current_guess
        self._guesses.append(last_guess)
        self._current_guess = WordleGuess()
        self._emit_all(WordleEvent.SUBMISSION_RESULT, last_guess)
