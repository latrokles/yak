import logging
import os
import sys

from pathlib import Path

YAKDIR = Path.home() / Path('.yak')
LOGFORMAT = '%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s'
LOGFILE = YAKDIR / 'yak.log'

HOME = os.getenv('HOME')
HISTORY = YAKDIR / 'yak.history'


def getenv_bool(name: str, default: bool = False) -> bool:
    def parse_bool(val: str|bool) -> bool:
        if isinstance(val, bool):
            return val
        return val.lower() in ('true', 't')
    return parse_bool(os.getenv(name, default))


def set_up_yakdir():
    if YAKDIR.exists():
        return
    print(f'creating yak dir: {YAKDIR}')
    YAKDIR.mkdir()


def get_logger(level: str):
    loglevel = getattr(logging, level)
    logging.basicConfig(filename=LOGFILE, level=loglevel, format=LOGFORMAT)
    return logging.getLogger()
