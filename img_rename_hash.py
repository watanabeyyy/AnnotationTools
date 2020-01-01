"""rename .png img by imghash 
"""
import os
import glob
import argparse
from shutil import move
from multiprocessing import Pool, freeze_support
from tqdm import tqdm
from PIL import Image
import imagehash


def rename_hash(file):
    output_dir = ""
    try:
        filename = os.path.splitext(os.path.basename(file))
        data = imagehash.whash(Image.open(file))
        path = os.path.join(output_dir, str(data)+filename[1])
        move(file, path)
    except:
        None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-i', '--input_dir',
                        default="",
                        help="")
    args = parser.parse_args()

    input_dir = args.input_dir
    files = glob.glob(os.path.join(input_dir, ""))
    freeze_support()  # windowsのおまじない
    pool = Pool(processes=8)
    with tqdm(total=len(files)) as t:
        for _ in pool.imap_unordered(rename_hash, files):
            t.update(1)
