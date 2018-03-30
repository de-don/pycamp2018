from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)
from time import perf_counter as pc

from task_11.cats import save_cat_and_print_hash, get_urls

count = 40
max_count_workers = 20

executors = {"Cats threads": ThreadPoolExecutor, "Cats process": ProcessPoolExecutor}


if __name__ == '__main__':
    urls = get_urls(count)
    for title, executor_class in executors.items():
        print("#" * 10, title, "#" * 10)

        for part in range(1, max_count_workers + 1):
            t = pc()
            with executor_class(max_workers=part) as executor:
                result = list(executor.map(save_cat_and_print_hash, urls))
                print(
                    f"{title} count = {part}.",
                    f"Count results: {len(result)}",
                    "Time:", pc() - t
                )
        print()