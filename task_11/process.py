from multiprocessing import Process


class MyProcess(Process):
    def __init__(self, autostart=False, queue=None, **kwargs):
        """Инициализация"""
        Process.__init__(self)
        self.queue = queue
        self.kwargs = kwargs
        if autostart:
            self.start()

    def run(self):
        pass


def wait_results(items):
    for item in items:
        item.join()


def get_results(queue, count):
    return [queue.get() for _ in range(count)]
