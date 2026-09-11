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

from PIL import Image


class Mandelbrot:
    """Represents the Mandelbrot set."""

    def __init__(self, width: int, height: int, max_iter: int = 50) -> None:
        self.width = width
        self.height = height
        self.max_iter = max_iter

    def get_point(self, x: float, y: float) -> bool:
        """Determines if a point is in the Mandelbrot set."""
        c = complex(x, y)
        z = 0
        for _ in range(self.max_iter):
            z = z * z + c
            if abs(z) > 2:
                return False
        return True

    def generate_image(self, bounds: tuple[float, float, float, float]) -> Image:
        """Generates an image of the Mandelbrot set within the given bounds."""
        img = Image.new('RGB', (self.width, self.height), "black")
        pixels = img.load()

        for i in range(self.width):
            for j in range(self.height):
                x = bounds[0] + (i / self.width) * (bounds[2] - bounds[0])
                y = bounds[1] + (j / self.height) * (bounds[3] - bounds[1])
                if self.get_point(x, y):
                    pixels[i, j] = (255, 255, 255)  # White for points in the set
                else:
                    pixels[i, j] = (0, 0, 0)  # Black for points outside the set

        return img

if __name__ == "__main__":
    mandelbrot = Mandelbrot(800, 600)
    print(mandelbrot.get_point(1, 0))  # Example usage
    img = mandelbrot.generate_image((-2, -1.5, 1, 1.5))
    img.show()