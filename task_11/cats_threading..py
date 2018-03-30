from time import perf_counter as pc

from task_11.cats import save_cat_and_print_hash, get_urls
from task_11.thread import MyThread, get_threads_results


class CatThread(MyThread):
    def run(self):
        self.result = save_cat_and_print_hash(self.kwargs['url'])


def main():
    count = 40
    max_count_threads = 20

    urls = get_urls(count)
    for part in range(1, max_count_threads):
        t = pc()
        results = []
        k = 0
        while k < count:
            # calc count threads
            part_size = min(count - k, part)
            urls_part = urls[k:k + part_size]
            k += part_size

            # create threads
            threads = [CatThread(autostart=True, url=url) for url in urls_part]
            results_iter = get_threads_results(threads)
            results.extend(list(results_iter))

        count_unique = len(set(results))
        print(
            f"Threads count = {part}.",
            f"Count results: {len(results)}(uniq: {len(count_unique)})",
            f"Time: {pc() - t}"
        )


if __name__ == "__main__":
    main()
