import asyncio
import logging
from typing import (
    Any,
    Dict,
    Callable,
    List,
    cast,
    MutableMapping,
    Tuple,
    Optional,
    Mapping,
)

from fwordle import wtypes, models, language
from fwordle.game.wordle_events import WordleAction, WordleEvent
from fwordle.game.wordle_guess import WordleGuess

_logger = logging.getLogger(__name__)


class Wordle(wtypes.Game):
    params: wtypes.GameParameters
    chosen_word: str

    _session_id: wtypes.SessionId
    _dictionary: language.LengthDictionary
    _current_guess: WordleGuess
    _guesses: List[WordleGuess]

    _action_map: Dict[WordleAction, Callable[[wtypes.PlayerId, Any], None]]
    _event_queue: "asyncio.Queue[wtypes.BroadcastEvent]"
    _players: List[models.Player]

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
            return (
                f"[S:{self._wordle._session_id}]{self.generate_debug()} {msg}",
                kwargs,
            )

        def generate_debug(self) -> str:
            if self.logger.isEnabledFor(logging.DEBUG):
                last_guess = ""
                if len(self._wordle._guesses) > 0:
                    last_guess = self._wordle._guesses[-1]
                return (
                    f"[word: {self._wordle.chosen_word}, last guess:"
                    f" {last_guess}]"
                )
            return ""

    def __init__(self, session_id: str, dictionary: language.LengthDictionary):
        self._session_id = session_id
        self._dictionary = dictionary
        self._current_guess = WordleGuess(1)
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

    def on_player_added(self, player: wtypes.Player):
        self._players.append(models.Player.from_impl(player))

        self._emit(player.id, WordleEvent.LETTER_ADDED, self._current_guess)
        self._emit_all(WordleEvent.PLAYER_CHANGED, self._players)

    def on_player_removed(self, removed_player_id: wtypes.PlayerId):
        self._players = [
            player for player in self._players if player.id != removed_player_id
        ]
        self._emit_all(WordleEvent.PLAYER_CHANGED, self._players)

    def set_parameters(self, game_parameters: wtypes.GameParameters):
        self.params = game_parameters
        self.chosen_word = self._dictionary.generate(self.params.word_length)

    def process_action(
        self, player: wtypes.PlayerId, player_action: wtypes.PlayerAction
    ):
        wordle_action = WordleAction[player_action.action]
        handler = self._action_map[wordle_action]
        handler(player, player_action.params)

    def event_queue(self) -> "asyncio.Queue[wtypes.BroadcastEvent]":
        return self._event_queue

    def _emit(
        self, player_id: wtypes.PlayerId, event: WordleEvent, params: Any
    ):
        self._log.debug("emitting event %s to player %s", event, player_id)
        self._event_queue.put_nowait(
            wtypes.BroadcastEvent(
                [player_id],
                wtypes.GameEvent(event.name, params),
            )
        )

    def _emit_all(self, event: WordleEvent, params: Any):
        self._log.debug("emitting event %s", event)
        self._event_queue.put_nowait(
            wtypes.BroadcastEvent(
                [wtypes.ALL_PLAYER_ID], wtypes.GameEvent(event.name, params)
            )
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
        submission_count = cast(int, params)

        # validation:
        # - can't submit guess if not long enough
        # - can't submit guess if all guesses already used up
        # - can't submit n-th guess if n-th guess already submitted
        if (
            len(self._current_guess) != self.params.word_length
            or len(self._guesses) >= self.params.max_guesses
            or len(self._guesses) != submission_count - 1
        ):
            self._log.error("rejecting bad submission %s", submission_count)
            return

        if not self._dictionary.is_word(self._current_guess.join()):
            self._emit_all(WordleEvent.SUBMISSION_NOT_A_WORD, submission_count)
            return

        last_guess = self._current_guess
        last_guess.verify(self.chosen_word)
        self._guesses.append(last_guess)
        self._current_guess = WordleGuess(submission_count + 1)
        self._emit_all(WordleEvent.SUBMISSION_RESULT, last_guess)
