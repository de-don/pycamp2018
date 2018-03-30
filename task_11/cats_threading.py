import logging
from time import perf_counter as pc

from cats import save_cat_and_print_hash, get_urls
from thread import MyThread, get_threads_results


class CatThread(MyThread):
    def run(self):
        self.result = save_cat_and_print_hash(self.kwargs['url'])


def main():
    logger = logging.getLogger(__name__)
    lvl = logger.level

    count = 5
    max_count_threads = 5

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
        logger.log(lvl,
                   f"Threads count = {part}. "
                   f"Count results: {len(results)}(uniq: {count_unique}) "
                   f"Time: {pc() - t}"
                   )


if __name__ == "__main__":
    main()
