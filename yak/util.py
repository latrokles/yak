import logging
import os
import sys

LOGFORMAT = '%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s'
LOGLEVEL = getattr(logging, os.getenv('LOGLEVEL', 'INFO'))

logging.basicConfig(level=LOGLEVEL, stream=sys.stdout, format=LOGFORMAT)

LOG = logging.getLogger()
