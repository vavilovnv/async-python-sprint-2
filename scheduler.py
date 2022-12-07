
def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Scheduler:
    def __init__(self, pool_size=10):
        self.pool_size = pool_size

    def schedule(self, task):
        pass

    def run(self):
        pass

    def restart(self):
        pass

    def stop(self):
        pass
