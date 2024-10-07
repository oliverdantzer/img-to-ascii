import image_to_str
import test_font_to_image
import numpy as np
import os
from filesystem import GENERATED_DIR, CHARSET

if __name__ == "__main__":
    img = test_font_to_image.test_char_to_image(" ", (100, 100))
    img.save(os.path.join(GENERATED_DIR, "char_test.png"))
    image = img.convert('L')
    print("Char brightness ", np.mean(np.array(image).flatten()))
    converter = image_to_str.Converter(image.size)
    char = converter.image_to_str(image)
    print(f"result: '{char}'")
    print("len: ", len(char))
