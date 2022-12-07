from utils import get_logger

logger = get_logger()


def create_file():
    with open('some_file.txt', 'w', encoding='UTF-8') as f:
        msg = 'File created.'
        f.write('%s\n', msg)
    logger.info(msg=msg)
