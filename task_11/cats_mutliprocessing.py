from multiprocessing import Process
from time import perf_counter as pc

from task_11.cats import save_cat_and_print_hash, get_urls

count = 100

if __name__ == '__main__':
    t = pc()
    procs = []
    for i, url in enumerate(get_urls(count)):
        proc = Process(
            target=save_cat_and_print_hash,
            args=("Process #%s" % (i + 1), url)
        )
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    print("Time:", pc() - t)

### 6.240751851000823 100 штук
