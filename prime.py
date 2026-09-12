import math
from numba import jit


@jit(cache=True)
def is_prime(num: int) -> bool:
    if num < 2:  # checks if a number is prime
        return False

    for i in range(
        2, int(math.sqrt(num)) + 1
    ):  # checks if a number is divisible by any number up to its square root
        if num % i == 0:
            return False

    return True


def generate_spiral(size):

    x, y = 0, 0
    coordinates = [(x, y)]

    return coordinates

if __name__ == "__main__":
    primes: set[int] = set()
    for n in range(2, 100000):  # range of prime numbers
        if is_prime(n):
            primes.add(n)

    print(primes)  # the list of primes

    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        ]

    print(generate_spiral(25)) 