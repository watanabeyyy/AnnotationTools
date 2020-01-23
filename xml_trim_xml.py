import os
import glob
import argparse
from tqdm import tqdm
import numpy as np
from utils.pascalvoc_xml_tools import create_xmldoc, save_xmldoc, read_xmldoc

parser = argparse.ArgumentParser(description="")
parser.add_argument('-i', '--xml_dir',
                    default="",
                    help="")
args = parser.parse_args()
xml_paths = glob.glob(os.path.join(args.xml_dir, "*.xml"))

for xmlpath in tqdm(xml_paths):
    info = read_xmldoc(xmlpath)
    folder = info[0]
    filename = info[1]
    path = info[2]
    height = int(info[3])
    width = int(info[4])
    depth = int(info[5])
    objects = info[6]

    tmp = np.zeros((height, width))
    for idx in range(len(objects)):
        label = objects[idx][0]
        xmin = int(float(objects[idx][1]))+1
        ymin = int(float(objects[idx][2]))+1
        xmax = int(float(objects[idx][3]))-1
        ymax = int(float(objects[idx][4]))-1

        # left line
        prev_cnt = 1000000
        while True:
            if xmin == xmax - 1:
                break
            flg = True
            cnt = 0
            for i in range(ymin, ymax):
                if tmp[i, xmin] == 1:
                    flg = False
                    cnt += 1
            if flg:
                break
            else:
                if cnt == prev_cnt:
                    break
                else:
                    prev_cnt = cnt
                    xmin += 1

        # up line
        prev_cnt = 1000000
        while True:
            if ymin == ymax - 1:
                break
            flg = True
            cnt = 0
            for i in range(xmin, xmax):
                if tmp[ymin, i] == 1:
                    flg = False
                    cnt += 1
            if flg:
                break
            else:
                if cnt == prev_cnt:
                    break
                else:
                    prev_cnt = cnt
                    ymin += 1

        # right line
        prev_cnt = 1000000
        while True:
            if xmax == xmin + 1:
                break
            flg = True
            cnt = 0
            for i in range(ymin, ymax):
                if tmp[i, xmax] == 1:
                    flg = False
                    cnt += 1
            if flg:
                break
            else:
                if cnt == prev_cnt:
                    break
                else:
                    prev_cnt = cnt
                    xmax -= 1

        # down line
        prev_cnt = 1000000
        while True:
            if ymax == ymin + 1:
                break
            flg = True
            cnt = 0
            for i in range(xmin, xmax):
                if tmp[ymax, i] == 1:
                    flg = False
                    cnt += 1
            if flg:
                break
            else:
                if cnt == prev_cnt:
                    break
                else:
                    prev_cnt = cnt
                    ymax -= 1

        tmp[ymin:ymax, xmin:xmax] = 1
        objects[idx][1] = xmin
        objects[idx][2] = ymin
        objects[idx][3] = xmax
        objects[idx][4] = ymax

    doc = create_xmldoc(folder, filename, path, height, width, depth, objects)
    save_xmldoc(doc, xmlpath)
