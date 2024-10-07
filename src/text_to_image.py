from PIL import Image, ImageDraw, ImageFont
from filesystem import TTF_FILEPATHS, GENERATED_DIR
import numpy as np
import os

terminal_font_aspect_ratio = 0.5

font_path = TTF_FILEPATHS[0]  # Hardcoded to first font in font folder


class Converter:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        FULL_SIZE_CHAR = "▓"
        image = Image.new("L", (width*2, height*2), 0)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, height)
        bbox = draw.textbbox((0, 0), FULL_SIZE_CHAR, font=font)

        self.x_offset = -bbox[0]
        # self.y_offset = -bbox[1]

        # draw.rectangle(bbox, outline="red")
        # draw.text((0, 0), "A", fill=255, font=font)
        # image.show()

        self.bbox_width = bbox[2] - bbox[0]
        self.bbox_height = bbox[3]

        # draw.rectangle(bbox, outline="red")
        # draw.rectangle((0, 0, size[0], size[1]), outline="blue")
        # # Ä
        # draw.text((0, 0), "▓", fill=255, font=font)
        # draw.text((0, 0), "Ä", fill=255, font=font)
        # image.save(os.path.join(GENERATED_DIR, "bbox.png"))

    def convert_char(self, char: str) -> Image.Image:
        assert len(char) == 1, "Only one character is allowed"

        background_color = 255
        image = Image.new(
            "L", (self.bbox_width, self.bbox_height), background_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, self.height)

        draw.text((self.x_offset, 0), char, fill=0, font=font)
        # Resize image
        image = image.resize((self.width, self.height))
        return image


def get_charset_image_vectors(charset: str, width: int, height: int) -> list[np.ndarray]:
    """
    Returns vector for each character in the charset containing its
    flattened and normalized image data.

    Args:
        charset (str): The set of characters to be converted.
        size (tuple[int, int]): The size of the images for each character.

    Returns:
        list[np.ndarray]: List of array representations of images of the characters, 
        flattened to 1D, normalized to [0, 1]. Shape: (len(charset), width*height)
    """
    text_to_image_converter = Converter(width, height)
    char_image_vectors = []
    for char in charset:
        image = text_to_image_converter.convert_char(char)
        vector = np.array(image).flatten() / 255.0
        char_image_vectors.append(vector)
    return char_image_vectors
