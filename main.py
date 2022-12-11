import time
from scheduler import Scheduler
from job import Job
from tasks import get_task
from utils import DEFAULT_DURATION, FUTURE_START_TIME, SCHEDULE_DURATION


if __name__ == '__main__':

    jobs = [
        Job(get_task('read_from_file'), tries=3),
        Job(get_task('create_file')),
        Job(get_task('write_to_file')),
        Job(get_task('read_from_file'), max_working_time=0.1),
        Job(get_task('delete_file')),
        Job(get_task('create_dir')),
        Job(get_task('delete_dir'), FUTURE_START_TIME, DEFAULT_DURATION + 10),
        Job(get_task('create_dir'))
    ]

    scheduler = Scheduler(pool_size=7)

    for job in jobs:
        scheduler.schedule(job)

    scheduler.run()
