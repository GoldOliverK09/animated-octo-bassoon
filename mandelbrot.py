"""
Contains functions for generating the Mandelbrot set.

Zn = (Zn-1)^2 + C where C is in the form of a + bi where a, b are real numbers

from PIL import Image

img = Image.new( 'RGB', (255,255), "black") # Create a new black image
pixels = img.load() # Create the pixel map
for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # Set the colour accordingly

img.show()
"""

import math

import numpy as np
from PIL import Image


class Mandelbrot:
    """Represents the Mandelbrot set."""

    def __init__(self, width: int, height: int, max_iter: int = 50) -> None:
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def get_point(self, x: float, y: float) -> float:
        """Returns a smooth escape value for a point."""

        c = complex(x, y)
        z = 0

        for iteration in range(self.max_iter):

            magnitude_squared = z.real * z.real + z.imag * z.imag

            if magnitude_squared > 4:
                magnitude = math.sqrt(magnitude_squared)

                smooth_iteration = (
                    iteration + 1 - math.log(math.log(magnitude)) / math.log(2)
                )

                return smooth_iteration

            z = z**2 + c

        return self.max_iter

    def generate_image(self, bounds: tuple[float, float, float, float]) -> Image.Image:
        """Generates an image of the Mandelbrot set within the given bounds."""

        x = bounds[0] + (np.arange(self.width) / self.width) * (bounds[2] - bounds[0])
        y = bounds[1] + (np.arange(self.height) / self.height) * (bounds[3] - bounds[1])
        c = x[np.newaxis, :] + 1j * y[:, np.newaxis]
        z = np.zeros_like(c)
        iterations = np.full(c.shape, self.max_iter, dtype=float)
        active = np.ones(c.shape, dtype=bool)

        for iteration in range(self.max_iter):
            magnitude_squared = z.real * z.real + z.imag * z.imag
            escaped = active & (magnitude_squared > 4)

            if escaped.any():
                magnitude = np.sqrt(magnitude_squared[escaped])
                iterations[escaped] = (
                    iteration + 1 - np.log(np.log(magnitude)) / np.log(2)
                )
                active[escaped] = False

            if not active.any():
                break

            z[active] = z[active] ** 2 + c[active]

        colours = np.array(
            (
                (0, 0, 255),
                (0, 255, 255),
                (180, 0, 255),
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 0),
            )
        )
        escaped = iterations != self.max_iter
        t = (iterations[escaped] * 0.08) % 1
        position = t * (len(colours) - 1)
        start = position.astype(int)
        blend = position - start
        pixels = np.zeros((*c.shape, 3), dtype=np.uint8)
        pixels[escaped] = (
            colours[start]
            + (colours[np.minimum(start + 1, len(colours) - 1)] - colours[start])
            * blend[:, None]
        ).astype(np.uint8)

        return Image.fromarray(pixels, mode="RGB")


if __name__ == "__main__":
    mandelbrot = Mandelbrot(1200, 1200, 100)
    img = mandelbrot.generate_image((-2, -1.5, 1, 1.5))
    img.show()
