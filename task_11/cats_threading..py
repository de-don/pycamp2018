from threading import Thread
from time import perf_counter as pc

from task_11.cats import save_cat_and_print_hash, get_urls

count = 100


class MyThread(Thread):
    def __init__(self, name, url):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        save_cat_and_print_hash(self.name, self.url)


if __name__ == '__main__':
    t = pc()
    threads = []
    for i, url in enumerate(get_urls(count)):
        thread = MyThread("Thread #%s" % (i + 1), url)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Time:", pc() - t)

### 5.864217779999308 100 штук
