import hashlib
import re
from threading import Thread
from time import perf_counter as pc

import requests

count = 40


class MyThread(Thread):
    def __init__(self, name, url):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        """Запуск потока"""
        res = requests.get(self.url)
        m = hashlib.md5()
        m.update(res.content)
        print(self.name, m.hexdigest())


if __name__ == '__main__':
    url_xml = f'http://thecatapi.com/api/images/get?format=xml&results_per_page={count}'
    res = requests.get(url_xml)
    cat_urls = re.findall(r'<url>\s*(.*?)\s*</url>', res.text)

    t = pc()
    threads = []
    for i, url in enumerate(cat_urls):
        thread = MyThread("Thread #%s" % (i + 1), url)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Time:", pc() - t)

### 4.322 40 штук
