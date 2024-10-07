from filesystem import ASSETS_DIR
from image_to_str import Converter
from PIL import Image
import numpy as np
import os
import time


if __name__ == '__main__':
    width = 50
    image_path = os.path.join(ASSETS_DIR, 'sample-images/lenna.webp')
    image = Image.open(image_path)
    image = image.resize((image.width, image.height))
    converter = Converter(image.size, (80, 40))
    print(converter.image_to_str(image))
    # start = time.time()
    # for i in range(100):
    #     image_str = converter.image_to_str(image)
    #     print(image_str)
    # print(f"Time taken: {time.time() - start} seconds")
