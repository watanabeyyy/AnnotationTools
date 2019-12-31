"""bitwise-not augument and save .png and pascalvoc-xml for labelimg
"""
import glob
import codecs
import cv2
import os
from tqdm import tqdm
import argparse
from xml.dom import minidom

parser = argparse.ArgumentParser(description="")
parser.add_argument('-i', '--img_input_dir',
                    default="",
                    help="")
parser.add_argument('-x', '--xml_input_dir',
                    default="",
                    help="")
parser.add_argument('-o', '--output_dir',
                    default="",
                    help="")
args = parser.parse_args()

img_input_dir = args.img_input_dir
xml_input_dir = args.xml_input_dir
output_dir = args.output_dir
paths = glob.glob(os.path.join(img_input_dir, "*.png"))
for path in tqdm(paths):
    filename = os.path.splitext(os.path.basename(path))[0]
    # xml
    doc = minidom.parse(os.path.join(xml_input_dir, filename + ".xml"))
    nodeList = doc.getElementsByTagName('filename')
    nodeList[0].childNodes[0].nodeValue = "r_"+filename+".png"
    nodeList = doc.getElementsByTagName('path')
    filepath = os.path.join(output_dir, "r_"+filename+".png")
    nodeList[0].childNodes[0].nodeValue = filepath
    nodeList = doc.getElementsByTagName("object")
    for node in nodeList:
        for child in node.childNodes:
            if child.nodeName == "name":
                label = child.childNodes[0].data
                if label == "white":
                    child.childNodes[0].nodeValue = 'black'
                elif label == "black":
                    child.childNodes[0].nodeValue = 'white'
                label = child.childNodes[0].data
    filepath = os.path.join(output_dir, "r_"+filename+".xml")
    f = codecs.open(filepath, 'wb', encoding='utf-8')
    doc.writexml(f, '', ' '*4, '\n', encoding='UTF-8')
    f.close()
    # img
    img = cv2.imread(path)
    img = cv2.bitwise_not(img)
    filepath = os.path.join(output_dir, "r_"+filename+".png")
    cv2.imwrite(filepath, img)
