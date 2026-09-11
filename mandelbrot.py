from PIL import Image
import math

"""
Contains functions for generating the Mandelbrot set.

Zn = (Zn-1)^2 + C where C is in the form of a + bi where a, b are real numbers
"""

"""
from PIL import Image

img = Image.new( 'RGB', (255,255), "black") # Create a new black image
pixels = img.load() # Create the pixel map
for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # Set the colour accordingly

img.show()
"""


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
                    iteration
                    + 1
                    - math.log(math.log(magnitude)) / math.log(2)
                )

                return smooth_iteration

            z = z * z + c

        return self.max_iter

    def generate_image(self, bounds: tuple[float, float, float, float]) -> Image:
        """Generates an image of the Mandelbrot set within the given bounds."""

        img = Image.new("RGB", (self.width, self.height), "black")
        pixels = img.load()

        for i in range(self.width):
            for j in range(self.height):

                x = bounds[0] + (i / self.width) * (bounds[2] - bounds[0])
                y = bounds[1] + (j / self.height) * (bounds[3] - bounds[1])

                iteration = self.get_point(x, y)

                if iteration == self.max_iter:
                    pixels[i, j] = (0, 0, 0)  # Points that didnt escape are black

                else:
                    t = (iteration * 0.08) % 1

                    if t < 0.2:
                        p = t / 0.2 #blue to cyan
                        red = 0
                        green = int(255 * p)
                        blue = 255

                    elif t < 0.4:
                        p = (t - 0.2) / 0.2 #cyan to purple
                        red = int(180 * p)
                        green = int(255 * (1 - p))
                        blue = 255

                    elif t < 0.6:
                        p = (t - 0.4) / 0.2 #purple to pink
                        red = 180 + int(75 * p)
                        green = 0
                        blue = int(255 * (1 - p))

                    elif t < 0.8:
                        p = (t - 0.6) / 0.2 #pink to orange
                        red = 255
                        green = int(165 * p)
                        blue = 0

                    else:
                        p = (t - 0.8) / 0.2 #orange to yellow
                        red = 255
                        green = 165 + int(90 * p)
                        blue = 0

                    pixels[i, j] = (red, green, blue)

        return img


if __name__ == "__main__":
    mandelbrot = Mandelbrot(1600, 1200, 200)
    print(mandelbrot.get_point(1, 0))  # Example usage
    img = mandelbrot.generate_image((-2, -1.5, 1, 1.5))
    img.show()