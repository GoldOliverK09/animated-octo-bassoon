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


def iter_spiral(count, radial_scale=1.0):
    """Yield polar coordinates along a golden-angle scatter spiral."""
    golden_angle = math.pi * (3 - math.sqrt(5))

    for index in range(count):
        angle = index * golden_angle
        radius = radial_scale * math.sqrt(index)
        yield angle, radius


def generate_spiral(count):
    return list(iter_spiral(count))


if __name__ == "__main__":

    point_count = 500_000
    initial_view_radius = 500
    all_coordinates = []
    prime_coordinates = []

    figure, axis = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    polar_axis = cast(PolarAxes, axis)
    all_points = polar_axis.scatter([], [], s=1, color="lightgray", label="All numbers")
    prime_points = polar_axis.scatter(
        [], [], s=4, color="crimson", label="Prime numbers"
    )
    polar_axis.grid(False)
    polar_axis.set_xticks([])
    polar_axis.set_yticks([])
    polar_axis.spines["polar"].set_visible(False)
    polar_axis.set_ylim(0, initial_view_radius)

    # Show the empty plot before starting the expensive calculation.
    plt.show(block=False)
    plt.pause(0.1)

    for number, polar_coordinate in enumerate(iter_spiral(point_count), start=1):
        all_coordinates.append(polar_coordinate)

        if is_prime(number):
            prime_coordinates.append(polar_coordinate)

        if number % 1_000 == 0 or number == point_count:
            # all_points.set_offsets(all_coordinates)
            prime_points.set_offsets(prime_coordinates)
            current_radius = all_coordinates[-1][1] + 1
            polar_axis.set_ylim(0, max(initial_view_radius, current_radius))
            figure.canvas.draw_idle()
            figure.canvas.flush_events()
            plt.pause(0.001)

    plt.show()
