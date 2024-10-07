import matplotlib.pyplot as plt
import text_to_image
import filesystem
import numpy as np
from PIL import Image

chars_image_vectors = text_to_image.get_charset_image_vectors(
    filesystem.CHARSET, 100, 100)
char_to_imagevec = {
    filesystem.CHARSET[i]: vec for i, vec in enumerate(chars_image_vectors)}

char_means = {}

for char in char_to_imagevec.keys():
    mean = np.mean(char_to_imagevec[char])
    char_means[char] = mean

# Create a histogram of the mean values
hist, bin_edges = np.histogram(
    list(char_means.values()), bins=10, range=(0, 1))


plt.hist(list(char_means.values()), bins=10, range=(0, 1))
plt.title('Histogram of Character Image Vector Means')
plt.xlabel('Mean Intensity')
plt.ylabel('Frequency')
plt.show()

ordered = sorted(char_means, key=lambda x: char_means[x])


def to_img(char: str):
    return Image.fromarray(np.array(char_to_imagevec[char]).reshape(100, 100) * 255)


# to_img(ordered[0]).show()
print(ordered[0], char_means[ordered[0]])

to_img(ordered[-1]).show()
print(ordered[-1], char_means[ordered[-1]])