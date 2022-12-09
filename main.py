import time

from scheduler import Scheduler
from job import Job
from tasks import create_dir, create_file, delete_dir, delete_file, read_from_file, write_to_file
from utils import DEFAULT_DURATION, FUTURE_START_TIME


if __name__ == '__main__':
    scheduler = Scheduler(pool_size=7)

    scheduler.schedule(Job(read_from_file, tries=3))
    scheduler.schedule(Job(create_file))
    scheduler.schedule(Job(write_to_file))
    scheduler.schedule(Job(read_from_file, max_working_time=0.1))
    scheduler.schedule(Job(delete_file))
    scheduler.schedule(Job(create_dir))
    scheduler.schedule(Job(delete_dir, FUTURE_START_TIME, DEFAULT_DURATION + 10))
    scheduler.schedule(Job(create_dir))

    scheduler.run()

