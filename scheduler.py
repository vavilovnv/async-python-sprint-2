import threading
from datetime import datetime
from uuid import uuid4

from job import Job
from tasks import get_task
from utils import get_job_data, load_jobs_data, get_logger, save_to_file


logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.job_manager = Job.run()
        self.queue, self.jobs_data = [], dict()
        self.load_jobs_status()

    def schedule(self, job: Job):
        task_name = job.task.__name__
        if self.pool_size >= len(self.queue) + 1:
            self.queue.append(job)
            if job.start_at and job.start_at > datetime.now():
                logger.warning('Task "%s" added to scheduling at %s', task_name, job.start_at)
            else:
                logger.info('Task "%s" is added to the schedule', task_name)
        else:
            logger.error('Tried to add task "%s" to the schedule, but the queue is full', task_name)

    def get_task(self):
        job = self.queue.pop(0)
        task_name = job.task.__name__
        if job.start_at and job.start_at < datetime.now():
            logger.warning('Tried to add task "%s" to the schedule, but time is expired', task_name)
            return
        if job.dependencies:
            for dependency in job.dependencies:
                if dependency in self.queue or any([th.is_alive() for th in dependency.thread]):
                    # logger.info('Task "%s" is waiting for dependency %s', task_name, dependency)
                    self.queue.append(job)
                    return
        return job

    def run(self):
        logger.info('>>>Starting schedule jobs.')
        while self.queue:
            job = self.get_task()
            if job:
                self.job_manager.send(job)
                #     (job.task, job.start_at, job.max_working_time, job.tries)
                # ))

    def load_jobs_status(self):
        for task in load_jobs_data():
            self.schedule(
                Job(get_task(task['name']),
                    task['start_at'],
                    task['max_working_time'],
                    task['tries'],
                    task['dependencies'])
            )

    def save_jobs_status(self):
        data = dict()
        while len(self.queue) > 0:
            try:
                job = self.queue.pop(0)
                data[uuid4().hex] = get_job_data(job)
            except (AttributeError, IndexError):
                break
        if len(data) > 0:
            save_to_file(data)
