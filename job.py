from datetime import datetime, timedelta
from typing import Callable
from uuid import uuid4
from utils import TIME_PATTERN


class Job:
    def __init__(self,
                 task: Callable,
                 start_at: str = "",
                 max_working_time: int = -1,
                 tries: int = 0,
                 dependencies: list = []):
        self.task = task()
        if start_at:
            self.start_at = datetime.strptime(start_at, TIME_PATTERN)
        else:
            self.start_at = None
        if max_working_time > 0:
            self.max_working_time = timedelta(seconds=max_working_time)
        else:
            self.max_working_time = None
        if self.start_at and self.max_working_time:
            self.finish_at = self.start_at + self.max_working_time
        elif self.max_working_time:
            self.finish_at = datetime.now() + self.max_working_time
        else:
            self.finish_at = None
        self.tries = tries
        self.dependencies = dependencies
        self.id = uuid4()

    def run(self):
        return next(self.task)

    def pause(self):
        pass

    def stop(self):
        pass
