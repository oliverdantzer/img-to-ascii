from filesystem import TTF_FILEPATHS
from text_to_image import Converter, get_charset_image_vectors
import numpy as np


def prune_charset_by_similarity(charset: str) -> str:
    SIZE = (8, 8)

    char_image_vectors = get_charset_image_vectors(charset, SIZE)

    def calculate_sad(image1, image2):
        sad = 0
        for i in range(len(image1)):
            for j in range(len(image1[0])):
                sad += abs(image1[i][j] - image2[i][j])
        return sad

    res = []
    for a in range(len(char_image_vectors)):
        for b in range(a+1, len(char_image_vectors)):
            sad = calculate_sad(char_image_vectors[a].reshape(
                SIZE), char_image_vectors[b].reshape(SIZE))
            res.append((charset[a], charset[b], sad))

    avg_sad = sum(sad for _, _, sad in res) / len(res)
    std_dev_sad = (sum((sad - avg_sad)**2 for _,
                   _, sad in res) / len(res))**0.5
    pruning_factor = 1

    pruned_charset = set(charset)

    for a, b, sad in res:
        if sad < avg_sad - std_dev_sad/pruning_factor:
            pruned_charset.discard(b)

    return "".join(list(pruned_charset))
