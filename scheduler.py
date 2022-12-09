import time
from datetime import datetime
from threading import Timer
from job import Job
from utils import get_logger


logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size - 1
        self.queue = []
        self.job_manager = Job.run()

    def schedule(self, job: Job):
        task_name = job.task.__name__
        if self.pool_size < len(self.queue):
            logger.error('Tried to add task "%s" to the schedule, but the queue is full', task_name)
            return
        if (job.start_at
                and job.start_at < datetime.now()):
            logger.warning('Tried to add task "%s" to the schedule, but time is expired', task_name)
            return
        if (job.start_at
                and job.start_at > datetime.now()):
            logger.warning('Task "%s" added to scheduling at %s', task_name, job.start_at)
            seconds = (job.start_at - datetime.now()).total_seconds()
            timer = Timer(seconds, self.queue.append, (job,))
            timer.start()
            self.queue.append(None)
            return
        self.queue.append(job)
        logger.info('Task "%s" is added to the schedule', task_name)

    def run(self):
        logger.info('Starting schedule jobs.')
        while True:
            job = self.queue.pop(0) if self.queue else None
            if job:
                self.job_manager.send(
                    (job.task, job.start_at, job.max_working_time, job.tries)
                )

    def restart(self):
        pass

    def stop(self):
        pass
