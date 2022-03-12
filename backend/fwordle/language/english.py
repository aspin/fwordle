from fwordle.language.length_dict import LengthDictionary


def load_length_dict(path: str) -> LengthDictionary:
    length_dict = LengthDictionary()
    with open(path) as f:
        for line in f:
            length_dict.add_word(line)

    return length_dict
