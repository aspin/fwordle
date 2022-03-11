from fwordle.serializer import Case


class App:
    empty_session_timeout_s = 30
    case = Case.CAMEL
    dictionary_path = (
        "/Users/kevin.chen/workspace/fwordle/backend/data_files/words_alpha.txt"
    )
