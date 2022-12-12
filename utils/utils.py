import json
import logging
import sys
from datetime import datetime, timedelta

URL_MOSCOW = 'https://code.s3.yandex.net/async-module/moscow-response.json'
ERR_MESSAGE_TEMPLATE = "Something wrong. Please contact with mentor."

SOME_FILE_NAME = 'some_file.txt'
JOBS_FILE_NAME = 'jobs_data.json'
DIR_NAME = 'some dir'
TIME_PATTERN = '%d.%m.%Y %H:%M:%S'

future_datetime = datetime.now() + timedelta(seconds=5)
DELAY_START_TIME = future_datetime.strftime(TIME_PATTERN)
DEFAULT_DURATION = 0.1


def get_logger() -> logging.Logger:
    """Настройки логгера для проекта."""

    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    )
    return logging.getLogger('scheduler')


def get_job_data(job):
    """Вспомогательная функция для получения данных задачи в удобном для
    сохранения в json формате."""

    start_at = job.start_at or ''
    if isinstance(start_at, datetime):
        start_at = start_at.strftime(TIME_PATTERN)
    return {
        'name': job.task.__name__,
        'start_at': start_at,
        'max_working_time': job.max_working_time,
        'tries': job.tries,
        'dependencies': []
    }


def load_json() -> dict:
    """Загрузка данных по задачам из json-файла."""

    try:
        with open(JOBS_FILE_NAME, 'r', encoding='UTF-8') as f:
            try:
                return json.load(f)
            except ValueError:
                return dict()
    except EnvironmentError:
        return dict()


def save_json(job_data: dict) -> None:
    """Сохранение данных по задачам в json-файл."""

    with open(JOBS_FILE_NAME, 'w', encoding='UTF-8') as f:
        json.dump(job_data, f)
