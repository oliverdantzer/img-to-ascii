import os
import glob

SRC_DIR = os.path.dirname(os.path.realpath(__file__))

ROOT_DIR = os.path.dirname(SRC_DIR)

ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')

GENERATED_DIR = os.path.join(ROOT_DIR, 'generated')

TTF_FILEPATHS = glob.glob(os.path.join(
    ASSETS_DIR, f'font{os.path.sep}*{os.path.sep}*.ttf'))

CHARSET = ""
with open(os.path.join(ASSETS_DIR, 'charset-pruned-manual.txt'), 'r', encoding="utf-8") as file:
    CHARSET = file.read()

