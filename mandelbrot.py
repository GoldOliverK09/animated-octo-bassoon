"""
Contains functions for generating the Mandelbrot set.

Zn = (Zn-1)^2 + C

C is in the form a + bi, where a and b are real numbers.
"""

import time
import math
import numpy as np

from PIL import Image
from numba import njit, prange


@njit(parallel=True, cache=True)
def calculate_mandelbrot(width, height, max_iter, bounds):
    x_min, y_min, x_max, y_max = bounds

    iterations = np.full((height, width), max_iter, dtype=np.float64)

    x_values = np.linspace(x_min, x_max, width)
    y_values = np.linspace(y_min, y_max, height)

    for py in prange(height):  # pylint: disable=not-an-iterable
        c_imag = y_values[py]

        for px in range(width):
            c_real = x_values[px]

            z_real = 0.0
            z_imag = 0.0

            for iteration in range(max_iter):
                z_real_squared = z_real * z_real
                z_imag_squared = z_imag * z_imag

                new_z_real = z_real_squared - z_imag_squared + c_real

                new_z_imag = 2.0 * z_real * z_imag + c_imag

                z_real = new_z_real
                z_imag = new_z_imag

                magnitude_squared = z_real * z_real + z_imag * z_imag

                if magnitude_squared > 4.0:
                    magnitude = math.sqrt(magnitude_squared)

                    smooth_iteration = (
                        iteration + 1 - math.log(math.log(magnitude)) / math.log(2.0)
                    )

                    iterations[py, px] = smooth_iteration
                    break

    return iterations


class Mandelbrot:
    def __init__(self, width, height, max_iter):
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def generate_image(self, bounds):
        iterations = calculate_mandelbrot(
            self.width, self.height, self.max_iter, bounds
        )

        palette = np.array(
            [
                (0, 0, 255),
                (0, 255, 255),
                (180, 0, 255),
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 0),
            ],
            dtype=np.float64,
        )

        escaped = iterations != self.max_iter

        image_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        if np.any(escaped):
            escaped_values = iterations[escaped]

            minimum = escaped_values.min()
            maximum = escaped_values.max()

            if maximum > minimum:
                normalized = (iterations - minimum) / (maximum - minimum)
            else:
                normalized = np.zeros_like(iterations)

            normalized = np.clip(normalized, 0.0, 1.0)

            palette_position = normalized * (len(palette) - 1)

            lower_index = np.floor(palette_position).astype(int)

            upper_index = np.minimum(lower_index + 1, len(palette) - 1)

            blend = palette_position - lower_index

            for channel in range(3):
                colour = (
                    palette[lower_index, channel] * (1.0 - blend)
                    + palette[upper_index, channel] * blend
                )

                image_array[:, :, channel] = np.where(escaped, colour, 0).astype(
                    np.uint8
                )

        return Image.fromarray(image_array, "RGB")


if __name__ == "__main__":
    # mandelbrot = Mandelbrot(width=16384, height=16384, max_iter=500)
    mandelbrot = Mandelbrot(width=4096, height=4096, max_iter=500)
    start_time = time.time()
    img = mandelbrot.generate_image((-2, -1.5, 1, 1.5))
    print(
        f"Time taken to initialize Mandelbrot: {time.time() - start_time:.2f} seconds"
    )

    # img.save("mandelbrot.png", "PNG")
    img.show()
