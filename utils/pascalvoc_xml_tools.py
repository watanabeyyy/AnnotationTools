"""create pascalvoc-sytle .xmlfile.
create xml and save xml.
This xml can be loaded from labelimg.
"""
import codecs
import os
from xml.dom import minidom


def create_xmldoc(folder, filename, path, height, width, depth, objects):
    """xmlファイルを作成する
    pascalvoc形式に合うようにxmlファイルを作成する

    Arguments:
        folder -- 画像があるフォルダ名
        filename -- 画像のファイル名
        path -- 画像のフルパス
        height -- 画像の高さ
        width  -- 画像の幅
        depth -- 画像のチャンネル数
        objects -- 物体のリスト
    Examples:
        objects = [label,xmin,ymin,xmax,ymax]]

    Returns:
        doc -- minidom.Document
    """
    #
    doc = minidom.Document()
    tree = doc.createElement('annotation')
    doc.appendChild(tree)
    ##
    branch = doc.createElement('folder')
    tree.appendChild(branch)
    text = doc.createTextNode(folder)
    branch.appendChild(text)
    ##
    branch = doc.createElement('filename')
    tree.appendChild(branch)
    text = doc.createTextNode(filename)
    branch.appendChild(text)
    ##
    branch = doc.createElement('path')
    tree.appendChild(branch)
    text = doc.createTextNode(path)
    branch.appendChild(text)
    ##
    branch = doc.createElement('source')
    tree.appendChild(branch)
    ###
    leaf = doc.createElement('database')
    branch.appendChild(leaf)
    text = doc.createTextNode('Unknown')
    leaf.appendChild(text)
    ##
    branch = doc.createElement('size')
    tree.appendChild(branch)
    ###
    leaf = doc.createElement('width')
    branch.appendChild(leaf)
    text = doc.createTextNode(str(width))
    leaf.appendChild(text)
    ###
    leaf = doc.createElement('height')
    branch.appendChild(leaf)
    text = doc.createTextNode(str(height))
    leaf.appendChild(text)
    ###
    leaf = doc.createElement('depth')
    branch.appendChild(leaf)
    text = doc.createTextNode(str(depth))
    leaf.appendChild(text)
    ##
    branch = doc.createElement('segmented')
    tree.appendChild(branch)
    text = doc.createTextNode('0')
    branch.appendChild(text)

    for i in range(len(objects)):
        name = objects[i][0]
        xmin = str(objects[i][1])
        ymin = str(objects[i][2])
        xmax = str(objects[i][3])
        ymax = str(objects[i][4])
        ##
        branch = doc.createElement('object')
        tree.appendChild(branch)
        ###
        leaf = doc.createElement('name')
        branch.appendChild(leaf)
        text = doc.createTextNode(name)
        leaf.appendChild(text)
        ###
        leaf = doc.createElement('pose')
        branch.appendChild(leaf)
        text = doc.createTextNode('Unspecified')
        leaf.appendChild(text)
        ###
        leaf = doc.createElement('truncated')
        branch.appendChild(leaf)
        text = doc.createTextNode('0')
        leaf.appendChild(text)
        ###
        leaf = doc.createElement('difficult')
        branch.appendChild(leaf)
        text = doc.createTextNode('0')
        leaf.appendChild(text)
        ###
        leaf = doc.createElement('bndbox')
        branch.appendChild(leaf)
        ####
        sub_leaf = doc.createElement('xmin')
        leaf.appendChild(sub_leaf)
        text = doc.createTextNode(xmin)
        sub_leaf.appendChild(text)
        ####
        sub_leaf = doc.createElement('ymin')
        leaf.appendChild(sub_leaf)
        text = doc.createTextNode(ymin)
        sub_leaf.appendChild(text)
        ####
        sub_leaf = doc.createElement('xmax')
        leaf.appendChild(sub_leaf)
        text = doc.createTextNode(xmax)
        sub_leaf.appendChild(text)
        ####
        sub_leaf = doc.createElement('ymax')
        leaf.appendChild(sub_leaf)
        text = doc.createTextNode(ymax)
        sub_leaf.appendChild(text)

    return doc


def save_xmldoc(xmldoc, filepath):
    """save xml

    Arguments:
        xmldoc -- minidom.Document
        filepath  -- xml save path
    """
    # Text encoding
    f = codecs.open(filepath, 'wb', encoding='utf-8')
    # XML header's encoding
    xmldoc.writexml(f, '', ' '*4, '\n', encoding='UTF-8')
    f.close()


def read_xmldoc(filepath):
    """read pascal-voc-style .xml

    Args:
        filepath : xml path
    Returns:
        out: list
    """
    out = []
    doc = minidom.parse(filepath)
    folder = doc.getElementsByTagName("folder")[0].firstChild.nodeValue
    filename = doc.getElementsByTagName("filename")[0].firstChild.nodeValue
    path = doc.getElementsByTagName("path")[0].firstChild.nodeValue
    out.append(folder)
    out.append(filename)
    out.append(path)

    size = doc.getElementsByTagName("size")[0]
    height = size.getElementsByTagName("height")[0].firstChild.nodeValue
    width = size.getElementsByTagName("width")[0].firstChild.nodeValue
    depth = size.getElementsByTagName("depth")[0].firstChild.nodeValue
    out.append(height)
    out.append(width)
    out.append(depth)

    object_list = []
    objects = doc.getElementsByTagName("object")
    for obj in objects:
        obj_info = []
        name = obj.getElementsByTagName("name")[0].firstChild.nodeValue
        bndbox = obj.getElementsByTagName("bndbox")[0]
        xmin = bndbox.getElementsByTagName("xmin")[0].firstChild.nodeValue
        ymin = bndbox.getElementsByTagName("ymin")[0].firstChild.nodeValue
        xmax = bndbox.getElementsByTagName("xmax")[0].firstChild.nodeValue
        ymax = bndbox.getElementsByTagName("ymax")[0].firstChild.nodeValue
        obj_info.append(name)
        obj_info.append(xmin)
        obj_info.append(ymin)
        obj_info.append(xmax)
        obj_info.append(ymax)
        object_list.append(obj_info)
    out.append(object_list)
    return out


if __name__ == '__main__':
    folder = "inputs"
    path = "a/a/a/a/0afa4ff4996e272b8d62e49932192572.png"
    filename = os.path.basename(path)
    height = 640
    width = 640
    depth = 3
    objects = [
        [
            "ball",
            100,
            100,
            300,
            300
        ],
        [
            "ball",
            200,
            200,
            400,
            400
        ]
    ]
    doc = create_xmldoc(folder, filename, path, height, width, depth, objects)
    save_xmldoc(doc, os.path.splitext(filename)[0] + '.xml')

    xml = read_xmldoc(os.path.splitext(filename)[0] + '.xml')
    print(xml)
