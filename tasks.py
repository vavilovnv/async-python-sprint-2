from pathlib import Path
from utils import get_logger, DIR_NAME, FILE_NAME

logger = get_logger()


def create_file():
    logger.info('Started creating file %s.', FILE_NAME)
    with open(FILE_NAME, 'w', encoding='UTF-8') as f:
        msg = f'File {FILE_NAME} created.'
        f.write(f'{msg}\n')
        yield
    logger.info(msg=msg)


def write_to_file():
    logger.info('Started writing to file %s.', FILE_NAME)
    with open(FILE_NAME, 'a', encoding='UTF-8') as f:
        f.writelines([f'Some text {i}\n' for i in range(10)])
        yield
    logger.info('Finished writing to file.')


def read_from_file():
    logger.info('Started reading file %s.', FILE_NAME)
    with open(FILE_NAME, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            logger.info(line)
            yield
    logger.info('Finished reading file.')


def create_dir():
    logger.info('Started creating dir.')
    for i in range(5):
        path = Path(f'{DIR_NAME} {i}')
        if not path.is_dir():
            path.mkdir()
            yield
    logger.info('Finished creating dir.')


def delete_dir():
    logger.info('Started deleting dir.')
    for i in range(5):
        path = Path(f'{DIR_NAME} {i}')
        if path.is_dir():
            path.rmdir()
            yield
    logger.info('Finished deleting dir.')
