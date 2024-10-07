import text_to_image
from abc import ABC, abstractmethod
from scipy.spatial import KDTree
import numpy as np
from typing import Any
import os
from filesystem import GENERATED_DIR
import math


def get_charset_image_vectors(charset: str, width: int, height: int) -> list[np.ndarray]:
    text_to_image_converter = text_to_image.Converter(
        width, height)
    char_image_vectors = []
    for char in charset:
        image = text_to_image_converter.convert_char(char)
        if char == "A":
            image.save(os.path.join(GENERATED_DIR, "A_charset.png"))
        if char == "◘":
            image.save(os.path.join(GENERATED_DIR, "◘_charset.png"))
        vector = np.array(image).flatten() / 255.0
        char_image_vectors.append(vector)
    return char_image_vectors


class ArrayToChar(ABC):
    def __init__(self, charset: str, char_images: list[np.ndarray]):
        super().__init__()
        self.charset = charset

    @abstractmethod
    def query(self, array: np.ndarray) -> str:
        pass


class ArrayToCharKDTree(ArrayToChar):
    def __init__(self, charset, char_images):
        super().__init__(charset, char_images)
        self.kd_tree = KDTree(char_images)

    def query(self, array) -> str:
        distance, index = self.kd_tree.query(array)
        return self.charset[index]


class ArrayToCharSAD(ArrayToChar):
    def __init__(self, charset, char_images):
        super().__init__(charset, char_images)
        self.char_images = char_images

    def query(self, array) -> str:
        def calculate_sad(vec1: np.ndarray, vec2: np.ndarray):
            # sum of all differences
            sad = 0
            for i in range(len(vec1)):
                sad += abs(vec1[i] - vec2[i])
            return sad
        min = float('inf')
        index = 0
        for i, char_image in enumerate(self.char_images):
            sad = calculate_sad(array.reshape(char_image.shape), char_image)
            if sad < min:
                min = sad
                index = i
        return self.charset[index]


class ArrayToCharMeanBrightness(ArrayToChar):
    def __init__(self, charset, width, height):
        self.charset = charset
        aspect_ratio = width / height
        char_image_vectors = get_charset_image_vectors(
            charset, math.ceil(100*aspect_ratio), 100)
        char_to_imagevec = {
            charset[i]: vec for i, vec in enumerate(char_image_vectors)}

        self.char_means: list[tuple[str, Any]] = []  # (char, mean)

        for char in char_to_imagevec.keys():
            mean = np.mean(char_to_imagevec[char])
            self.char_means.append((char, mean))

        self.char_means.sort(key=lambda x: x[1])
        print("Brightness min and max: ", min(self.char_means, key=lambda x: x[1]), max(
            self.char_means, key=lambda x: x[1]))

    def query(self, array: np.ndarray) -> str:
        mean = np.mean(array)
        # for char, char_mean in self.char_means:
        #     if char == "A":
        #         print(f"Mean of 'A': {char_mean}, vs queried mean {mean}")
        #     if char_mean == mean:
        #         return char
        # return "f"
        l, r = 0, len(self.char_means) - 1

        while l <= r:
            mid = (l + r) // 2
            if mean < self.char_means[mid][1]:
                r = mid - 1
            elif mean > self.char_means[mid][1]:
                l = mid + 1
            else:
                return self.char_means[mid][0]  # Exact match found

        # If no exact match, return the closest match.
        if l >= len(self.char_means):
            return self.char_means[r][0]
        if r < 0:
            return self.char_means[l][0]

        # Determine which of l or r is closer to the target mean
        if abs(self.char_means[l][1] - mean) < abs(self.char_means[r][1] - mean):
            return self.char_means[l][0]
        else:
            return self.char_means[r][0]
