import time
from pathlib import Path
from utils import get_logger, DIR_NAME, FILE_NAME

logger = get_logger()


def create_file():
    time.sleep(0.3)
    with open(FILE_NAME, 'w', encoding='UTF-8') as f:
        msg = f'File {FILE_NAME} created.'
        f.write(f'{msg}\n')
    logger.info(msg=msg)


def write_to_file():
    time.sleep(0.3)
    with open(FILE_NAME, 'a', encoding='UTF-8') as f:
        f.writelines([f'Some text {i + 1}\n' for i in range(10)])
    logger.info('Finished writing to file.')


def read_from_file():
    time.sleep(0.3)
    with open(FILE_NAME, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            logger.info(line.strip())
    logger.info('Finished reading file.')


def delete_file():
    time.sleep(0.3)
    path = Path(FILE_NAME)
    if path.is_file():
        path.unlink()
        logger.info('Deleted %s.', path)
    logger.info('Finished deleting file.')


def create_dir():
    time.sleep(0.3)
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if not path.is_dir():
            path.mkdir()
            logger.info('Created %s.', path)
    logger.info('Finished creating dir.')


def delete_dir():
    time.sleep(0.3)
    for i in range(5):
        path = Path(f'{DIR_NAME} {i + 1}')
        if path.is_dir():
            path.rmdir()
            logger.info('Deleted %s.', path)
    logger.info('Finished deleting dir.')
