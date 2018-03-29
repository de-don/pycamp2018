from threading import Thread
from time import perf_counter as pc

from Crypto.Util.number import getPrime

bits = 2 ** 12
count = 20


class MyThread(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        """Запуск потока"""
        prime = getPrime(bits)
        print(self.name, prime)


if __name__ == "__main__":
    t = pc()
    threads = []
    for i in range(count):
        thread = MyThread("Thread #%s" % (i + 1))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Time:", pc() - t)
