from multiprocessing import Queue
from time import perf_counter as pc

from task_11.cats import save_cat_and_print_hash, get_urls
from task_11.process import MyProcess, wait_results, get_results

count = 40
max_count_process = 20


class CatProcess(MyProcess):
    def run(self):
        """Запуск"""
        hash = save_cat_and_print_hash(self.kwargs['url'])
        # сохраняем результат в очередь
        self.queue.put(hash)


if __name__ == '__main__':
    urls = get_urls(count)
    for part in range(1, max_count_process+1):
        t = pc()
        queue = Queue()
        k = 0
        while k < count:
            # calc count threads
            part_size = min(count - k, part)
            urls_part = urls[k:k + part_size]
            k += part_size

            # create threads
            processes = [CatProcess(autostart=True, queue=queue, url=url) for url in urls_part]
            wait_results(processes)

        results = get_results(queue, count)
        count_unique = len(set(results))
        print(
            f"Processes count = {part}.",
            f"Count results: {len(results)}(uniq: {count_unique})",
            f"Time: {pc() - t}"
        )
