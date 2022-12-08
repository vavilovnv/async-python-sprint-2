import time
from pathlib import Path
from utils import get_logger, DEFAULT_DURATION, DIR_NAME, FILE_NAME

logger = get_logger()


def create_file():
    with open(FILE_NAME, 'w', encoding='UTF-8') as f:
        msg = f'File {FILE_NAME} created.'
        f.write(f'{msg}\n')
        time.sleep(DEFAULT_DURATION)
        yield True
    logger.info(msg=msg)


def write_to_file():
    with open(FILE_NAME, 'a', encoding='UTF-8') as f:
        f.writelines([f'Some text {i + 1}\n' for i in range(10)])
        time.sleep(DEFAULT_DURATION)
        yield True
    logger.info('Finished writing to file.')


def read_from_file():
    with open(FILE_NAME, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            logger.info(line)
            time.sleep(DEFAULT_DURATION)
            yield True
    logger.info('Finished reading file.')


def create_dir():
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if not path.is_dir():
            path.mkdir()
            logger.info('Created %s.', path)
            time.sleep(DEFAULT_DURATION)
            yield True
    logger.info('Finished creating dir.')


def delete_dir():
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if path.is_dir():
            path.rmdir()
            logger.info('Deleted %s.', path)
            time.sleep(DEFAULT_DURATION)
            yield True
    logger.info('Finished deleting dir.')
