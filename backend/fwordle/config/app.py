from dataclasses import dataclass

from fwordle.serializer import Case


@dataclass
class App:
    empty_session_timeout_s: int = 30
    case: Case = Case.CAMEL
    dictionary_path: str = (
        "/Users/kevin.chen/workspace/fwordle/backend/data_files/words_alpha.txt"
    )
