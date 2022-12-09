from datetime import datetime, timedelta
from multiprocessing import Process
from typing import Callable
from uuid import uuid4
from utils import get_logger, TIME_PATTERN


logger = get_logger()


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Job:
    def __init__(self,
                 task: Callable,
                 start_at: str = "",
                 max_working_time: int = -1,
                 tries: int = 0,
                 dependencies: list = []):
        self.task = task
        if start_at:
            self.start_at = datetime.strptime(start_at, TIME_PATTERN)
        else:
            self.start_at = None
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies

    @staticmethod
    @coroutine
    def run():
        while True:
            try:
                task, start_at, max_working_time, tries = (yield)
                task_name = task.__name__
                logger.info('Task "%s" started.', task_name)
                if max_working_time > 0:
                    process = Process(target=task)
                    process.start()
                    process.join(max_working_time)
                    if process.is_alive():
                        process.terminate()
                        logger.warning('Task "%s" terminated.', task_name)
                else:
                    task()
                    logger.info('Task "%s" finished.', task_name)
                tries = 0
            except Exception as error:
                logger.error(error)
                while tries:
                    tries -= 1
                    logger.warning('Task "%s" restarted.', task_name)
                    try:
                        task()
                        logger.info('Task "%s" successful finished.', task_name)
                    except Exception as error:
                        logger.error(error)

    def pause(self):
        pass

    def stop(self):
        pass
