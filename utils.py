import logging
import sys
from datetime import datetime, timedelta


FILE_NAME = 'some_file.txt'
DIR_NAME = 'some dir'

TIME_PATTERN = '%d.%m.%Y %H:%M:%S'

future_datetime = datetime.now() + timedelta(seconds=5)
FUTURE_START_TIME = future_datetime.strftime(TIME_PATTERN)
DEFAULT_DURATION = 1


def get_logger():
    logger = logging.getLogger('scheduler')
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    )
    return logger
