from threading import Thread


class MyThread(Thread):
    result = None

    def __init__(self, autostart=False, **kwargs):
        """Инициализация"""
        Thread.__init__(self)
        self.kwargs = kwargs
        if autostart:
            self.start()

    def run(self):
        pass


def get_threads_results(items):
    for item in items:
        item.join()
        yield item.result
