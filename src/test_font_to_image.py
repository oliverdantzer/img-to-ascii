import text_to_image
from PIL import Image
from filesystem import GENERATED_DIR
import os


def test_char_to_image(char, size: tuple[int, int]):
    converter = text_to_image.Converter(size[0], size[1])
    image = converter.convert_char(char)
    return image


def test_char_to_image_sizes(char, sizes: list[int]):
    for size in sizes:
        converter = text_to_image.Converter(size, size)
        image = converter.convert_char(char)
        image.save(os.path.join(GENERATED_DIR, f"char_{size}.png"))


def test_str_to_image(test_str: str, size: tuple[int, int]):
    converter = text_to_image.Converter(size[0], size[1])

    lines = test_str.split("\n")
    width = size[0] * max(len(line) for line in lines)
    height = size[1] * len(lines)
    str_image = Image.new('RGB', (width, height))

    # Paste each character's image into the new image
    y_offset = 0
    for line in lines:
        x_offset = 0
        for char in line:
            char_image = converter.convert_char(char)
            str_image.paste(char_image, (x_offset, y_offset))
            x_offset += size[0]
        y_offset += size[1]
    return str_image


if __name__ == "__main__":
    teststr = """
Traceback (most recent call last):
    File "src/test_font_to_image.py", line 1, in <module>
        from filesystem import▓▓▓▓ CHARSET, TTF_FILEPATHS
"""
    # test_str_to_image(teststr, (10, 50)).show()
    # test_char_to_image("Ä", (100, 100)).show()
    sizes = [1, 5, 10, 20]
    test_char_to_image_sizes("A", sizes)
    
