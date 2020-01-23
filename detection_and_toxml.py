"""detection result to xml for auto annotateion.
"""
import os
import glob
import argparse
import cv2
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from utils.pascalvoc_xml_tools import create_xmldoc, save_xmldoc
from utils.detection import DetectionModel_PB, inference_tta
from utils.detection_tools import non_max_suppression, overlay_result


parser = argparse.ArgumentParser(description="")
parser.add_argument('-i', '--input_dir',
                    default="",
                    help="")
parser.add_argument('-o', '--output_dir',
                    default="",
                    help="")
args = parser.parse_args()

detection_model = DetectionModel_PB(
    "exported_graphs/frozen_inference_graph.pb")
# loop img dir
input_dir = args.input_dir
paths = glob.glob(os.path.join(input_dir, "*.png"))
for path in tqdm(paths):
    raw_img = cv2.imread(path)
    # detection
    objects = inference_tta(detection_model, raw_img)
    objects = non_max_suppression(objects, 0.5, raw_img)

    new_objects = []
    for ball in objects:
        # label
        label = ball[1]
        info = []
        info.append(label)

        h, w, c = raw_img.shape
        # bounding box
        #x> yv
        info.append(ball[2][0]*w)
        info.append(ball[2][1]*h)
        info.append(ball[2][2]*w)
        info.append(ball[2][3]*h)
        new_objects.append(info)

    # create xml
    folder = "inputs"
    filename = os.path.basename(path)
    height, width, depth = h, w, c
    doc = create_xmldoc(
        folder, filename, path, height, width, depth, new_objects)
    # save xml
    output_dir = args.output_dir
    save_xmldoc(doc, os.path.join(
        output_dir, os.path.splitext(filename)[0] + '.xml'))
