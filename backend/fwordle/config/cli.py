import argparse

from fwordle.config import App


def parse_args() -> App:
    parser = argparse.ArgumentParser(
        description="fwordle backend websockets server"
    )

    parser.add_argument(
        "--dictionary-path",
        type=str,
        required=True,
        help="path of English dictionary data file",
    )

    args = parser.parse_args()
    return App(dictionary_path=args.dictionary_path)
