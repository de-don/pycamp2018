from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
from time import perf_counter as pc

from Crypto.Random import atfork
from Crypto.Util.number import getPrime

bits = 2 ** 11
count = 40
max_count_workers = 20


def get_prime(count_primes):
    atfork()
    return getPrime(bits)


executors = {
    "Crypto threads": ThreadPoolExecutor,
    "Crypto process": ProcessPoolExecutor
}

if __name__ == "__main__":

    for title, executor_class in executors.items():
        print("#" * 10, title, "#" * 10)

        for part in range(1, max_count_workers + 1):
            t = pc()
            with executor_class(max_workers=part) as executor:
                result = list(executor.map(get_prime, [5] * count))
                print(
                    f"{title} count = {part}.",
                    f"Count results: {len(result)}",
                    "Time:", pc() - t
                )
        print()