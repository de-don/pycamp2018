from multiprocessing import Queue
from time import perf_counter as pc

from Crypto.Util.number import getPrime

from task_11.process import MyProcess, wait_results, get_results

bits = 2 ** 11
count = 40
max_count_process = 20


class PrimeProcess(MyProcess):
    def run(self):
        """Запуск"""
        prime = getPrime(bits)
        # сохраняем результат в очередь
        self.queue.put(prime)


if __name__ == "__main__":
    for part in range(1, max_count_process + 1):
        t = pc()
        queue = Queue()
        k = 0
        while k < count:
            # calc count threads
            part_size = min(count - k, part)
            k += part_size

            # create threads
            processes = [PrimeProcess(autostart=True, queue=queue) for i in range(part_size)]
            wait_results(processes)

        results = sorted(get_results(queue, count))
        print(f"Processes count = {part}.", f"Count results: {len(results)}", "Time:", pc() - t)
