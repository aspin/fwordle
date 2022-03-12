from dataclasses import dataclass

from fwordle.serializer import Case


@dataclass
class App:
    dictionary_path: str
    empty_session_timeout_s: int = 30
    case: Case = Case.CAMEL
