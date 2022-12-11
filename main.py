import time
from scheduler import Scheduler
from job import Job
from utils import DELAY_FINISH_TIME, DELAY_START_TIME, SCHEDULE_DURATION, future_datetime


if __name__ == '__main__':

    create_dir = Job('create_dir', start_at=DELAY_START_TIME)
    create_file = Job('create_file')
    write_to_file = Job('write_to_file')
    delete_file = Job('delete_file', start_at=DELAY_FINISH_TIME)

    jobs = [
        # Job('read_from_file', tries=3),
        Job('read_from_file', dependencies=[create_file, write_to_file]),
        create_file,
        write_to_file,
        # Job('read_from_file', max_working_time=0.1),
        delete_file,
        create_dir,
        Job('delete_dir', dependencies=[create_dir]),
        # Job('create_file'),
        # Job('read_from_file')
    ]

    scheduler = Scheduler(pool_size=7)

    for job in jobs:
        scheduler.schedule(job)

    scheduler.run()
