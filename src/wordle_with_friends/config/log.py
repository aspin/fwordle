import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] [%(asctime)s] %(message)s",
        stream=sys.stdout,
    )
