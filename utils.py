import logging


def get_logger():
    logger = logging.getLogger('scheduler')
    logging.basicConfig(
        filename='scheduler_log.log',
        level=logging.DEBUG,
        filemode='w',
        format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    )
    return logger
