import numpy as np
from numpy.typing import ArrayLike
from filesystem import CHARSET, TTF_FILEPATHS, GENERATED_DIR
import text_to_image
from PIL import Image
import time
from skimage import exposure
import math
from array_to_char import ArrayToChar, ArrayToCharKDTree, ArrayToCharSAD, ArrayToCharMeanBrightness
from prune_charset_by_similarity import prune_charset_by_similarity
import os


def hist_eq(image: np.ndarray):
    # hist, bins = exposure.histogram(image, nbins=256, normalize=False)
    # # append any remaining 0 values to the histogram
    # hist = np.hstack((hist, np.zeros((255 - bins[-1]))))
    # cdf = 255*(hist/hist.sum()).cumsum()
    # equalized = cdf[image].astype(np.uint8)

    # return equalized
    return exposure.equalize_adapthist(image, clip_limit=0.01)


PIXEL_GROUPING_ASPECT_RATIO = 1/2


class Converter:
    def __init__(self, image_size: tuple[int, int], str_size: tuple[int, int] = (1, 1)):
        # charset = prune_charset_by_similarity(CHARSET)
        charset = CHARSET
        self.original_image_size = image_size
        self.str_size = str_size
        self.pixel_group_width = math.ceil(image_size[0] / str_size[0])
        self.pixel_group_height = math.ceil(image_size[1] / str_size[1])
        print("Pixel group size: ", self.pixel_group_width,
              self.pixel_group_height)
        self.resized_image_size = (
            str_size[0] * self.pixel_group_width,
            str_size[1] * self.pixel_group_height
        )

        # char_image_vectors = get_charset_image_vectors(
        #     charset, self.pixel_group_width, self.pixel_group_height)

        self.array_to_char_data_structure: ArrayToChar = ArrayToCharMeanBrightness(
            charset, self.pixel_group_width, self.pixel_group_height)

    def pixel_group_to_char(self, pixel_group: np.ndarray):
        vector = pixel_group.flatten()
        return self.array_to_char_data_structure.query(vector)

    def image_to_str(self, image: Image.Image):
        image = image.convert('L')
        image = image.resize(self.resized_image_size)

        # normalized array representation of image.
        # shape is (height, width)
        image_array = np.array(image) / 255.0
        
        #expand range of pixel values to [0, 1]
        image_array = ((image_array - image_array.min()) / (image_array.max()-image_array.min()))

        # histogram equalization
        image_array = exposure.equalize_adapthist(image_array, clip_limit=0.06)

        brightness_modifier = 0.4
        image_array = np.clip(image_array + brightness_modifier, 0, 1)
        print("Avg. brightness of image: ", np.mean(image_array))

        Image.fromarray((image_array * 255).astype(np.uint8)
                        ).save(os.path.join(GENERATED_DIR, "postprocess.png"))

        image_str = ""
        for y in range(self.str_size[1]):
            row = ""
            for x in range(self.str_size[0]):
                pixel_group = image_array[y * self.pixel_group_height:(y + 1) * self.pixel_group_height,
                                          x * self.pixel_group_width:(x + 1) * self.pixel_group_width]
                assert pixel_group.shape[0] == self.pixel_group_height and pixel_group.shape[1] == self.pixel_group_width
                char = self.pixel_group_to_char(pixel_group)
                row += char
                # if char == "•":
                # if char == "±":
                #     print(pixel_group)
            image_str += row + \
                ("\n" if (x, y) !=
                 (self.str_size[0] - 1, self.str_size[1] - 1) else "")
        return image_str
