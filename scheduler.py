from datetime import datetime
from job import Job
from utils import get_job_data, load_json, get_logger, save_json


logger = get_logger()


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.job_manager = Job.run()
        self.queue = []

    @staticmethod
    def load_from_file():
        jobs_list, dependencies = [], dict()
        for key, task in load_json().items():
            jobs_list.append(
                Job(
                    uid=key,
                    task=task['name'],
                    start_at=task['start_at'],
                    max_working_time=task['max_working_time'],
                    tries=task['tries'],
                    dependencies=[]
                )
            )
            dependencies[key] = task['dependencies']
        for job in jobs_list:
            job.dependencies = list(filter(
                lambda x: x.uid in dependencies[job.uid],
                jobs_list))
        return jobs_list

    @staticmethod
    def save_to_file(queue):
        data = dict()
        for job in queue:
            job_data = get_job_data(job)
            for dependency in job.dependencies:
                if dependency in queue:
                    job_data['dependencies'].append(dependency.uid)
            data[job.uid] = job_data
        if len(data) > 0:
            save_json(data)

    def schedule(self, job_list: list[Job]):
        self.queue = self.load_from_file()
        for job in job_list:
            self.queue.append(job)
            task_name = job.task.__name__
            if self.pool_size < len(self.queue):
                logger.error('Tried to add task "%s" to the schedule, but the queue is full', task_name)
                continue
            if job.start_at and job.start_at > datetime.now():
                logger.warning('Task "%s" added to scheduling at %s', task_name, job.start_at)
            else:
                logger.info('Task "%s" is added to the schedule', task_name)

    def get_job(self):
        job = self.queue.pop(0)
        task_name = job.task.__name__
        if job.start_at and job.start_at < datetime.now():
            logger.warning('Tried to add task "%s" to the schedule, but time is expired', task_name)
            return
        if job.dependencies:
            for dependency in job.dependencies:
                if dependency in self.queue or dependency.worker and dependency.worker.is_alive():
                    self.queue.append(job)
                    return
        return job

    def run(self):
        logger.info('>>>Starting schedule jobs.')
        count_jobs = 0
        while self.queue and count_jobs < self.pool_size:
            job = self.get_job()
            if job:
                count_jobs += 1
                self.job_manager.send(job)
        self.save_to_file(self.queue)
