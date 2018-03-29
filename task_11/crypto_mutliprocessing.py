from multiprocessing import Process
from multiprocessing.sharedctypes import Value, Array
from time import perf_counter as pc
from ctypes import c_char_p

from Crypto.Util.number import getPrime

bits = 2 ** 8
count = 40


class MyProcess(Process):
    result = None

    def __init__(self, value, autostart=False):
        """Инициализация"""
        Process.__init__(self)
        self.value = value
        if autostart:
            self.start()

    def run(self):
        """Запуск"""
        prime = getPrime(bits)
        self.value.value = prime
        #print(c_char_p(prime), prime)


def wait_and_get_results(items):
    for item in items:
        item.join()


if __name__ == "__main__":
    for part in range(1, 21):
        t = pc()
        results = [Value(c_char_p) for i in range(count)]
        k = 0
        while k < count:
            part_size = min(count - k, part)
            process = [MyProcess(value=results[k+i], autostart=True) for i in range(part_size)]
            wait_and_get_results(process)
            k += part_size
        print(results[4].value)
        res = results[:]
        print(f"Part size = {part}.", f"Count results: {len(res)}", "Time:", pc() - t, res)
