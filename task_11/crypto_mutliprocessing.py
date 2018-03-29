from multiprocessing import Process, Queue
from time import perf_counter as pc

from Crypto.Util.number import getPrime

bits = 2 ** 11
count = 40


class MyProcess(Process):
    result = None

    def __init__(self, queue, autostart=False):
        """Инициализация"""
        Process.__init__(self)
        self.queue = queue
        if autostart:
            self.start()

    def run(self):
        """Запуск"""
        prime = getPrime(bits)
        self.queue.put(prime)


def wait_results(items):
    for item in items:
        item.join()


if __name__ == "__main__":
    for part in range(1, 21):
        t = pc()
        queue = Queue()
        k = 0
        while k < count:
            part_size = min(count - k, part)
            process = [MyProcess(queue=queue, autostart=True) for i in range(part_size)]
            wait_results(process)
            k += part_size
        results = [queue.get() for _ in range(count)]
        print(f"Processes count = {part}.", f"Count results: {len(results)}", "Time:", pc() - t)
