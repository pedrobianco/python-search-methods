from PIL import Image
from numpy import array


class ImageCore:

    def __init__(self, image_path):
        """
        Image core.

        Download sample maze image: http://www.mazegenerator.net/
        Reference 1: http://code.activestate.com/recipes/577591-conversion-of-pil-image-and-numpy-array/
        """
        self.image = Image.open(image_path)
        self.image_array = array(self.image)
