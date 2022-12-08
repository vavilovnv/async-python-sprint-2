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
        self.pool_size = pool_size - 1
        self.queue = []

    def schedule(self, job: Job):
        task_name, uid = job.task.__name__, job.id
        if self.pool_size < len(self.queue):
            logger.error('Tried to add task %s uid %s to the schedule, but the queue is full', task_name, uid)
            return
        if (job.start_at
                and job.start_at < datetime.now()):
            logger.warning('Tried to add task %s uid %s to the schedule, but time is expired', task_name, uid)
            return
        if (job.start_at
                and job.start_at > datetime.now()):
            logger.warning('Task %s uid %s added to scheduling at %s', task_name, uid, job.start_at)
            seconds = (job.start_at - datetime.now()).total_seconds()
            timer = Timer(seconds, self.queue.append, (job,))
            timer.start()
            return
        self.queue.append(job)
        logger.info('Task %s uid %s is added to the schedule', task_name, uid)

    @staticmethod
    def _execute_job(job: Job):
        if not job:
            return False
        task_name, uid = job.task.__name__, job.id
        if (job.finish_at
                and job.finish_at < datetime.now()):
            logger.warning('Time task %s uid %s is expired', task_name, uid)
            return False
        logger.info('Task task %s uid %s running.', task_name, uid)
        try:
            result = job.run()
        except StopIteration:
            logger.info('Task %s uid %s finished.', task_name, uid)
            return False
        return result

    def run(self):
        logger.info('Starting schedule jobs.')
        while True:
            job = self.queue.pop(0) if self.queue else None
            if self._execute_job(job):
                self.queue.append(job)
            time.sleep(0.1)

    def restart(self):
        pass

    def stop(self):
        pass
