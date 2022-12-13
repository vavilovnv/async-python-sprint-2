import pathlib as pl
import unittest

from job import Job
from scheduler import Scheduler
from utils.utils import JOBS_FILE_NAME, load_json


class SchedulerTest(unittest.TestCase):
    """Тестирование методов класса Scheduler."""

    SCHEDULER = Scheduler()
    PATH = pl.Path(JOBS_FILE_NAME).resolve()
    COUNT_EXECUTED_JOBS = 3

    @staticmethod
    def assertFileNotExist(path):
        if not path.is_file():
            raise AssertionError(f'Файл не существует: {str(path)}')

    def test_1_add_to_schedule(self):
        """Тестирование метода добавления задач в расписание планировщика."""

        job_list = [
            Job('create_file'),
            Job('read_from_file'),
            Job('write_to_file'),
            Job('delete_file'),
            Job('get_whether')
        ]
        jobs_amount = len(job_list)
        self.SCHEDULER.schedule(job_list)
        self.assertEqual(
            len(self.SCHEDULER.queue),
            jobs_amount,
            f'Количество запланированных задач не равно {jobs_amount}:')

    def test_2_save_jobs_to_file(self):
        """Тестирование метода сохранения невыполненных задач в файл."""

        count_saved_jobs = (len(self.SCHEDULER.queue)
                            - self.COUNT_EXECUTED_JOBS)
        self.SCHEDULER.save_to_file(
            self.SCHEDULER.queue[self.COUNT_EXECUTED_JOBS:]
        )
        self.assertFileNotExist(self.PATH)
        self.assertEqual(
            len(load_json()),
            count_saved_jobs,
            f'Количество сохраненных задач не равно {count_saved_jobs}:')

    def test_3_load_jobs_from_file(self):
        """Тестирование метода загрузки задач из файла."""

        count_saved_jobs = (len(self.SCHEDULER.queue)
                            - self.COUNT_EXECUTED_JOBS)
        job_list = self.SCHEDULER.load_from_file()
        self.assertEqual(
            len(job_list),
            count_saved_jobs,
            f'Количество загр)уженных задач не равно {count_saved_jobs}:'
        )

    def test_4_run_jobs(self):
        """Тестирование метода исполнения задач планировщиком."""

        self.SCHEDULER.schedule([])
        self.SCHEDULER.run()
        self.assertTrue(
            len(self.SCHEDULER.queue) == 0,
            'Очередь задач не пуста:'
        )
        self.assertTrue(len(load_json()) == 0, 'Файл с задачами не пуст:')


if __name__ == '__main__':
    unittest.main()
