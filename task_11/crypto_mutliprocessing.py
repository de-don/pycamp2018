from multiprocessing import Process
from time import perf_counter as pc

from Crypto.Util.number import getPrime

bits = 2 ** 12
count = 20

def print_prime(name):
    prime = getPrime(bits)
    print(name, prime)


if __name__ == "__main__":
    t = pc()
    procs = []

    for i in range(count):
        name = "Process #%s" % (i + 1)
        proc = Process(target=print_prime, args=(name,))
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    print("Time:", pc() - t)
