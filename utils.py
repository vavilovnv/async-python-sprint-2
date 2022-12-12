import json
import logging
import sys
from datetime import datetime, timedelta


SOME_FILE_NAME = 'some_file.txt'
JOBS_FILE_NAME = 'jobs_data.json'
DIR_NAME = 'some dir'

TIME_PATTERN = '%d.%m.%Y %H:%M:%S'

future_datetime = datetime.now() + timedelta(seconds=5)
future_datetime2 = datetime.now() + timedelta(seconds=10)
DELAY_START_TIME = future_datetime.strftime(TIME_PATTERN)
DELAY_FINISH_TIME = future_datetime.strftime(TIME_PATTERN)
DEFAULT_DURATION = 0.3
SCHEDULE_DURATION = 1


def get_logger():
    logger = logging.getLogger('scheduler')
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    )
    return logger


def get_job_data(job):
    start_at = job.start_at
    if isinstance(start_at, datetime):
        start_at = start_at.strftime(TIME_PATTERN)
    return {
            'name': job.task.__name__,
            'start_at': start_at,
            'max_working_time': job.max_working_time,
            'tries': job.tries,
            'dependencies': []
        }


def load_json():
    try:
        with open(JOBS_FILE_NAME, 'r', encoding='UTF-8') as f:
            try:
                return json.load(f)

            except ValueError:
                return dict()
    except EnvironmentError:
        return dict()


def save_json(job_data):
    with open(JOBS_FILE_NAME, 'w', encoding='UTF-8') as f:
        json.dump(job_data, f)
