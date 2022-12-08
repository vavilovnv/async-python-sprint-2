import time
from datetime import datetime
from threading import Timer
from job import Job
from utils import get_logger


logger = get_logger()


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.queue = []

    def schedule(self, task: Job):
        if self.pool_size <= len(self.queue):
            logger.error('Queue is full')
            return
        if (task.start_at
                and task.start_at < datetime.now()):
            logger.warning('Time task %s is expired', task.id)
            return
        if (task.start_at
                and task.finish_at > datetime.now()):
            logger.info('Task %s added to scheduling at %s', task.id, task.start_at)
            seconds = (task.start_at - datetime.now()).total_seconds()
            timer = Timer(seconds, self.queue.append, (task,))
            timer.start()
            return
        self.queue.append(task)

    @staticmethod
    def _execute_task(task: Job):
        if not task:
            return
        if (task.finish_at
                and task.finish_at < datetime.now()):
            logger.warning('Time task %s is expired', task.id)
            return
        logger.info('Task %s running.', task.id)
        try:
            result = task.run()
        except StopIteration:
            logger.info('Task %s finished.', task.id)
            return
        return result

    def run(self):
        logger.info('Starting schedule jobs.')
        while self.queue:
            task = self.queue.pop(0)
            if self._execute_task(task):
                self.queue.append(task)
            time.sleep(0.3)

    def restart(self):
        pass

    def stop(self):
        pass
