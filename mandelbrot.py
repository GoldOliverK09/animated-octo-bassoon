"""
Contains functions for generating the Mandelbrot set.

Zn = (Zn-1)^2 + C

C is in the form a + bi, where a and b are real numbers.
"""

import time
import math
import numpy as np

from PIL import Image
from numba import jit, prange


@jit(parallel=True, cache=True)
def calculate_mandelbrot(
    image_width: int,
    image_height: int,
    max_iter: int,
    bounds: tuple,
) -> np.ndarray:
    """
    Calculate the Mandelbrot set for a given image size and bounds.
    """
    left, top, view_width, view_height = bounds

    iterations = np.full((image_height, image_width), max_iter, dtype=np.float64)

    x_values = np.linspace(left, left + view_width, image_width)
    y_values = np.linspace(top, top - view_height, image_height)

    for py in prange(image_height):  # pylint: disable=not-an-iterable
        c_imag = y_values[py]

        for px in range(image_width):
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
    """
    Class for rendering the Mandelbrot set.
    """

    def __init__(self, width: int, height: int, max_iter: int) -> None:
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def generate_image(self, bounds: tuple) -> Image.Image:
        """This function generates the Mandelbrot set image based on the provided bounds."""
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
                (255, 255, 255),
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
    print("Generating Mandelbrot set...")
    # mandelbrot = Mandelbrot(width=16384, height=16384, max_iter=500)
    size = 8
    mandelbrot = Mandelbrot(width=1024 * size, height=1024 * size, max_iter=100 * size)
    print("Mandelbrot set initialised.")
    start_time = time.time()
    img = mandelbrot.generate_image((-2, 1.5, 3, 3))

    print(f"Time taken to generate Mandelbrot: {time.time() - start_time:.2f} seconds")
    start_time = time.time()

    img.save("mandelbrot.png", "PNG")
    print(f"Time taken to save Mandelbrot: {time.time() - start_time:.2f} seconds")
    # img.show()
