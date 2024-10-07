from PIL import Image
import numpy as np


def moving_avg():
    def sample():
        # avg is 0.5, range is [0.45, 0.55]
        return 0.1 * np.random.rand(5, 5) + 0.45 * np.ones((5, 5))

    actual_mean = 0.5

    acc = sample()

    for i in range(1, 100):
        new_sample = sample()
        # acc = acc * (i-1)/i + new_sample * 1/i
        print(abs(actual_mean - np.mean(acc)))

    print(acc)


moving_avg()
