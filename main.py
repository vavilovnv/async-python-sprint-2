from scheduler import Scheduler
from tasks import create_file


if __name__ == '__main__':
    scheduler = Scheduler(pool_size=5)
    scheduler(create_file)
