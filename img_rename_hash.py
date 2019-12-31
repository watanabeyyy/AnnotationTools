"""rename .png img by imghash 
"""
import os
import glob
from PIL import Image
import argparse
from shutil import move
from tqdm import tqdm
import imagehash

parser = argparse.ArgumentParser(description="")
parser.add_argument('-i', '--input_dir',
                    default="",
                    help="")
args = parser.parse_args()

input_dir = args.input_dir
files = glob.glob(os.path.join(input_dir, "*png"))

for file in tqdm(files):
    filename = os.path.splitext(os.path.basename(file))
    data = imagehash.whash(Image.open(file))
    path = os.path.join(input_dir, str(data)+filename[1])
    move(file, path)
