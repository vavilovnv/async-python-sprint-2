import threading
from datetime import datetime
from uuid import uuid4

from job import Job
from tasks import get_task
from utils import get_job_data, load_jobs_data, get_logger, save_to_file


logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size - 1
        self.job_manager = Job.run()
        self.stop_jobs = threading.Event()
        self.queue, self.jobs_data = [], dict()
        self.load_jobs_status()

    def schedule(self, job: Job):
        task_name = job.task.__name__
        if len(self.queue) > self.pool_size:
            logger.error('Tried to add task "%s" to the schedule, but the queue is full', task_name)
            return
        if job.start_at:
            if job.start_at < datetime.now():
                logger.warning('Tried to add task "%s" to the schedule, but time is expired', task_name)
                return
        self.queue.append(job)
        if job.start_at and job.start_at > datetime.now():
            logger.warning('Task "%s" added to scheduling at %s', task_name, job.start_at)
        else:
            logger.info('Task "%s" is added to the schedule', task_name)

    def run(self):
        logger.info('>>>Starting schedule jobs.')
        while self.queue:
            job = self.queue.pop(0)
            self.job_manager.send(
                (job.task, job.start_at, job.max_working_time, job.tries)
            )

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
