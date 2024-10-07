import cv2

def dhash(image, hash_size=8):
    resized = cv2.resize(image, (hash_size + 1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(h1, h2):
    return bin(h1 ^ h2).count('1')

def image_similarity(image1, image2):
    hash1 = dhash(image1)
    hash2 = dhash(image2)
    return hamming_distance(hash1, hash2)

# Example usage
image1 = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)

similarity = image_similarity(image1, image2)
print("Similarity:", similarity)