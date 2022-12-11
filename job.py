import time
from datetime import datetime
from threading import Timer, Thread
from tasks import get_task
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
                 task: str,
                 start_at: str = "",
                 max_working_time: int = -1,
                 tries: int = 0,
                 dependencies: list = []):
        self.task = get_task(task)
        if start_at:
            self.start_at = datetime.strptime(start_at, TIME_PATTERN)
        else:
            self.start_at = None
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies
        self.thread = []

    @staticmethod
    def sleep_seconds(seconds):
        time.sleep(seconds)

    @staticmethod
    def delay_thread(task, seconds):
        Job.sleep_seconds(seconds)
        task()

    @staticmethod
    @coroutine
    def run():
        while True:
            try:
                # task, start_at, max_working_time, tries = (yield)
                job = (yield)
                task_name = job.task.__name__
                if job.start_at and job.start_at > datetime.now():
                    logger.info('Task "%s" starts at %s.', task_name, job.start_at)
                    seconds = (job.start_at - datetime.now()).total_seconds()
                    timer = Timer(seconds, job.task)
                    timer.start()
                    timer.join(job.max_working_time)
                    job.thread.append(timer)
                else:
                    logger.info('Task "%s" started.', task_name)
                    thread = Thread(target=job.task)
                    thread.start()
                    thread.join(job.max_working_time)
                    job.thread.append(thread)
                tries = 0
            except GeneratorExit:
                logger.info('Finished schedule jobs.')
                raise
            except Exception as error:
                logger.error(error)
                while tries:
                    tries -= 1
                    logger.warning('Task "%s" restarted.', task_name)
                    try:
                        job.task()
                        logger.info('Task "%s" successful finished.', task_name)
                    except Exception as error:
                        logger.error(error)

    def pause(self):
        pass

    def stop(self):
        pass
