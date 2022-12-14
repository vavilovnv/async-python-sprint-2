from datetime import datetime
from multiprocessing import Process
from threading import Thread, Timer
from typing import Generator
from uuid import uuid4

from tasks import get_task
from utils.utils import TIME_PATTERN, get_logger

logger = get_logger()


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Job:
    """Класс описывающий задачу планировщика и её методы."""

    def __init__(self,
                 task: str,
                 uid: str = '',
                 start_at: str = '',
                 max_working_time: int = -1,
                 tries: int = 0,
                 dependencies: list = None):
        self.task = get_task(task)
        if start_at:
            self.start_at = datetime.strptime(start_at, TIME_PATTERN)
        else:
            self.start_at = None
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies or []
        self.uid = uid if uid else uuid4().hex
        self.worker = None

    @staticmethod
    def __execute_job(job: 'Job') -> None:
        """Функция создает процесс или поток в зависимости от параметров
        задачи и запускает его на исполнение. Возвращает процесс или поток
        для дальнейшего отслеживания его состояния."""

        task_name = job.task.__name__
        if job.start_at and job.start_at > datetime.now():
            seconds = (job.start_at - datetime.now()).total_seconds()
            logger.info('Task "%s" starts at %s.', task_name, job.start_at)
            worker = Timer(seconds, job.task)
            worker.start()
        else:
            logger.info('Task "%s" started.', task_name)
            if job.max_working_time >= 0:
                worker = Process(target=job.task)
                worker.start()
                worker.join(job.max_working_time)
                if worker.is_alive():
                    worker.terminate()
                    logger.warning('Task "%s" was terminated.', task_name)
            else:
                worker = Thread(target=job.task)
                worker.start()
                worker.join()
        job.worker = worker

    @staticmethod
    @coroutine
    def run() -> Generator[None, 'Job', None]:
        """Корутина для запуска задач на исполнение."""

        while job := (yield):
            try:
                Job.__execute_job(job)
            except GeneratorExit:
                logger.info('>>>Finished schedule jobs.')
                raise
            except Exception as error:
                logger.error(error)
                while job.tries > 0:
                    job.tries -= 1
                    task_name = job.task.__name__
                    logger.warning('Task "%s" restarted.', task_name)
                    try:
                        Job.__execute_job(job)
                        logger.info(
                            'Task "%s" successful finished.',
                            task_name
                        )
                    except Exception as error:
                        logger.error(error)
