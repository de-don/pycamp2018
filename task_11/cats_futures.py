import logging
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)
from time import perf_counter as pc

from cats import save_cat_and_print_hash, get_urls


def main():
    logger = logging.getLogger(__name__)
    lvl = logger.level

    count = 5
    max_count_workers = 5

    executors = {"Cats threads": ThreadPoolExecutor, "Cats process": ProcessPoolExecutor}

    urls = get_urls(count)
    for title, executor_class in executors.items():
        logger.log(lvl, ("#" * 10) + title + ("#" * 10))

        for part in range(1, max_count_workers + 1):
            t = pc()
            with executor_class(max_workers=part) as executor:
                result = list(executor.map(save_cat_and_print_hash, urls))
                logger.log(lvl,
                           f"{title} count = {part}. "
                           f"Count results: {len(result)} "
                           f"Time:{(pc() - t)}"
                           )
        logger.log(lvl, "")


if __name__ == '__main__':
    main()
