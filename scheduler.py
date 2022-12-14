from datetime import datetime
from typing import Optional

from job import Job
from utils.data_classes import Task
from utils.utils import get_job_data, get_logger, load_json, save_json

logger = get_logger()


class Scheduler:
    """Класс описывающий планировщик задач и его методы."""

    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.job_manager = Job.run()
        self.queue = []

    @staticmethod
    def load_from_file() -> list[Job]:
        """Метод для импорта данных из json-файла в список задач
        планировщика. Восстановление зависимостей выполняется по uid задач."""

        jobs_list, dependencies = [], dict()
        for key, raw_task in load_json().items():
            task = Task.parse_obj(raw_task)
            jobs_list.append(
                Job(
                    uid=key,
                    task=task.name,
                    start_at=task.start_at,
                    max_working_time=task.max_working_time,
                    tries=task.tries,
                    dependencies=[]
                )
            )
            dependencies[key] = task.dependencies
        for job in jobs_list:
            job.dependencies = [j for j in jobs_list
                                if j.uid in dependencies[job.uid]]
        return jobs_list

    @staticmethod
    def save_to_file(queue: list[Job]) -> None:
        """Метод для экспорта в json-файл задач, которые не поместились в
        pool_size планировщика для исполнения при следующем запуске."""

        data = dict()
        for job in queue:
            job_data = get_job_data(job)
            for dependency in job.dependencies:
                if dependency in queue:
                    job_data['dependencies'].append(dependency.uid)
            data[job.uid] = job_data
        save_json(data)

    def schedule(self, job_list: list[Job]) -> None:
        """Постановка задач в очередь. Сперва из json-файла читаются
        сохраненные ранее задачи, которые не поместились в pool_size
        планировщика. В очередь можно добавить любое количество задач, но за
        один запуск планировщика будет обработано только то количество задач,
        которое соответствует pool_size планировщика. Задачи, которые не были
        обработаны сохраняются в json-файл для исполнения при следующем
        запуске планировщика."""

        self.queue = self.load_from_file()
        for job in job_list:
            self.queue.append(job)
            task_name = job.task.__name__
            if self.pool_size < len(self.queue):
                logger.error(
                    'Tried schedule "%s", but the queue is full',
                    task_name
                )
                continue
            if job.start_at and job.start_at > datetime.now():
                logger.warning(
                    'Task "%s" added to scheduling at %s',
                    task_name,
                    job.start_at
                )
            else:
                logger.info('Task "%s" is added to the schedule', task_name)

    def get_job(self) -> Optional[Job]:
        """Метод управляющий получением задач из очереди. Если задача
        просрочена, она удаляется из очереди и не передается на исполнение
        планировщику. Если у задачи есть зависимости, проверяется -
        завершились ли их процессы/потоки. Если да, задача передается на
        исполнение планировщику, если нет, задача возвращается в очередь."""

        job = self.queue.pop(0)
        task_name = job.task.__name__
        if job.start_at and job.start_at < datetime.now():
            logger.warning(
                'Tried to add task "%s" to the schedule, but time is expired',
                task_name
            )
            return None
        if job.dependencies:
            for dependency in job.dependencies:
                if (dependency in self.queue
                        or dependency.worker
                        and dependency.worker.is_alive()):
                    self.queue.append(job)
                    return None
        return job

    def run(self) -> None:
        """Метод запускающий планировщик в работу. Изначально я реализовал его
         в бесконечном цикле. Но к планировщику есть ряд требований по
         условию задания и я немного сломал голову, как их лучше реализовать.

         Моя идея в том, что планировщик исполняет задания пока они есть в
         очереди или пока количество задач не превысит pool_size. Иначе он
         останавливается. Если в очереди остались не обработанные задачи, они
         дампятся в файл, для того, чтобы их можно было запустить на
         исполнение перед новыми задачами при перезапуске планировщика. Т.е.
         методы Schedule и Run у планировщика позволяют реализовать в модуле
         Main произвольную логику. Например, можно поместить метод Run в
         бесконечный цикл. Либо запускать его на исполнение только тогда,
         когда в очередь при помощи Schedule добавляются новые задачи."""

        count = 0
        if self.queue:
            logger.info('>>>Starting schedule jobs.')
        while self.queue and count < self.pool_size:
            job = self.get_job()
            if job:
                count += 1
                self.job_manager.send(job)
        self.save_to_file(self.queue)
