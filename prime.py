import math
from typing import cast

from numba import jit
import matplotlib.pyplot as plt
from matplotlib.projections.polar import PolarAxes


@jit(cache=True)
def is_prime(num: int) -> bool:
    if num < 2:
        return False

    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False

    return True


def generate_spiral(size):

    x, y = 0, 0
    spiral_coordinates = [(x, y)]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right  # up  # left  # down

    direction = 0
    step_length = 1

    while len(spiral_coordinates) < size:

        for _ in range(2):

            dx, dy = directions[direction]

            for _ in range(step_length):

                if len(spiral_coordinates) >= size:
                    break

                x += dx
                y += dy

                spiral_coordinates.append((x, y))

            direction = (direction + 1) % 4

        step_length += 1

    return spiral_coordinates


if __name__ == "__main__":

    # Generate primes
    primes: set[int] = set()

    for n in range(2, 100000):
        if is_prime(n):
            primes.add(n)

    # Generate spiral coordinates
    coordinates = generate_spiral(10000)

    # Connect numbers to coordinates
    prime_coordinates = [
        coordinate
        for number, coordinate in enumerate(coordinates, start=1)
        if number in primes
    ]

    angles = [math.atan2(y, x) for x, y in coordinates]
    radii = [math.hypot(x, y) for x, y in coordinates]
    prime_angles = [math.atan2(y, x) for x, y in prime_coordinates]
    prime_radii = [math.hypot(x, y) for x, y in prime_coordinates]

    figure, axis = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    polar_axis = cast(PolarAxes, axis)
    #polar_axis.scatter(angles, radii, s=8, color="lightgray", label="All numbers")
    polar_axis.scatter(
        prime_angles,
        prime_radii,
        s=12,
        color="crimson",
        label="Prime numbers",
    )
    polar_axis.set_theta_zero_location("E")
    polar_axis.set_theta_direction(1)
    polar_axis.set_title("Ulam Spiral on a Circular Grid", pad=20)
    polar_axis.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    plt.show()
