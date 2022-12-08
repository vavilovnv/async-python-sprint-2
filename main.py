from scheduler import Scheduler
from job import Job
from tasks import create_dir, create_file, delete_dir, read_from_file, write_to_file


if __name__ == '__main__':
    scheduler = Scheduler(pool_size=5)

    scheduler.schedule(Job(create_file))
    scheduler.schedule(Job(write_to_file))
    scheduler.schedule(Job(read_from_file))
    scheduler.schedule(Job(create_dir))
    scheduler.schedule(Job(delete_dir))

    scheduler.run()
