from time import perf_counter as pc

from Crypto.Util.number import getPrime

from task_11.thread import MyThread, get_threads_results

bits = 2 ** 11
count = 40
max_count_threads = 20


class PrimeThread(MyThread):
    def run(self):
        """Запуск"""
        prime = getPrime(bits)
        self.result = prime


if __name__ == "__main__":
    for part in range(1, max_count_threads):
        t = pc()
        results = []
        k = 0
        while k < count:
            # calc count threads
            part_size = min(count - k, part)
            k += part_size

            # create threads
            threads = [PrimeThread(autostart=True) for i in range(part_size)]
            results_iter = get_threads_results(threads)
            results.extend(list(results_iter))

        results.sort()
        print(f"Threads count = {part}.", f"Count results: {len(results)}", "Time:", pc() - t)
