from threading import Thread
from time import perf_counter as pc

from Crypto.Util.number import getPrime

bits = 2 ** 10
count = 40


class MyThread(Thread):
    result = None

    def __init__(self, autostart=False):
        """Инициализация"""
        Thread.__init__(self)
        if autostart:
            self.start()

    def run(self):
        """Запуск"""
        prime = getPrime(bits)
        self.result = prime


def wait_and_get_results(items):
    for item in items:
        item.join()
        yield item.result


if __name__ == "__main__":
    for part in range(1, 21):
        t = pc()
        results = []
        k = 0
        while k < count:
            part_size = min(count - k, part)
            threads = [MyThread(autostart=True) for i in range(part_size)]
            results_iter = wait_and_get_results(threads)
            results.extend(list(results_iter))
            k += part_size

        results.sort()
        print(f"Threads count = {part}.", f"Count results: {len(results)}", "Time:", pc() - t, results)
