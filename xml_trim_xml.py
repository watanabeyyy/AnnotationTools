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

        while True:
            line_sum = []
            # left line
            line_sum.append(np.sum(tmp[ymin:ymax, xmin]))
            # up line
            line_sum.append(np.sum(tmp[ymin, xmin:xmax]))
            # right line
            line_sum.append(np.sum(tmp[ymin:ymax, xmax]))
            # down line
            line_sum.append(np.sum(tmp[ymax, xmin:xmax]))
            line_sum = np.array(line_sum)
            if np.max(line_sum) == 0:
                break
            max_id = np.argmax(line_sum)
            if max_id == 0:
                # left line
                xmin += 1
            elif max_id == 1:
                # up line
                ymin += 1
            elif max_id == 2:
                # right line
                xmax -= 1
            elif max_id == 3:
                # down line
                ymax -= 1

        tmp[ymin:ymax, xmin:xmax] = 1
        objects[idx][1] = xmin
        objects[idx][2] = ymin
        objects[idx][3] = xmax
        objects[idx][4] = ymax

    doc = create_xmldoc(folder, filename, path, height, width, depth, objects)
    save_xmldoc(doc, xmlpath)
