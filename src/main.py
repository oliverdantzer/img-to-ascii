import os

if __name__ == '__main__':
    IMG_FOLDER_PATH = '../assets/sample-images/'

    filenames = []
    for filename in os.listdir(IMG_FOLDER_PATH):
        if os.path.isfile(os.path.join(IMG_FOLDER_PATH, filename)):
            filenames.append(filename)