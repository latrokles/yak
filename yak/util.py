import logging
import os
import sys

from pathlib import Path

YAKDIR = Path.home() / Path('.yak')
LOGFORMAT = '%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s'
LOGLEVEL = getattr(logging, os.getenv('LOGLEVEL', 'DEBUG'))
LOGFILE = YAKDIR / 'yak.log'


def set_up_yakdir():
    if YAKDIR.exists():
        return
    print(f'creating yak dir: {YAKDIR}')
    YAKDIR.mkdir()


def get_logger():
    logging.basicConfig(filename=LOGFILE, level=LOGLEVEL, format=LOGFORMAT)
    return logging.getLogger()
