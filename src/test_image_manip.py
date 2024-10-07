from skimage import exposure
from filesystem import ASSETS_DIR
import os
import PIL.Image as Image
import numpy as np

image_path = os.path.join(ASSETS_DIR, 'sample-images/mountain.webp')
image = Image.open(image_path).convert('L')
image_array = np.array(image)
print(image_array)
image_array = image_array / 255.0  # normalize to [0, 1]
print(image_array)
image_array = exposure.equalize_adapthist(image_array, clip_limit=0.03)

print(image_array)
im2 = Image.fromarray(image_array * 255)
im2.show()
