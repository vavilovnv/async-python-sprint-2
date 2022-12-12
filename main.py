import time
from scheduler import Scheduler
from job import Job
from utils import DELAY_FINISH_TIME, DELAY_START_TIME, SCHEDULE_DURATION, future_datetime


if __name__ == '__main__':

    create_file_job = Job('create_file')
    read_from_file_job = Job('read_from_file', tries=3, dependencies=[create_file_job])
    write_to_file_job = Job('write_to_file')
    delete_file_job = Job('delete_file', dependencies=[create_file_job, write_to_file_job, read_from_file_job])
    create_dir_job = Job('create_dir', start_at=DELAY_START_TIME)
    delete_dir_job = Job('delete_dir', dependencies=[create_dir_job])

    scheduler = Scheduler(pool_size=7)

    scheduler.schedule([
        delete_file_job,
        read_from_file_job,
        create_file_job,
        write_to_file_job,
        read_from_file_job,
        create_dir_job,
        delete_dir_job
    ])
    scheduler.run()
