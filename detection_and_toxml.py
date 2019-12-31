"""detection result to xml for auto annotateion.
"""
import tensorflow as tf


def load_model():
    """load detection model.
    Note:
        .pb model must be created by Tensorflow Object Detection API
    """
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile('./exported_graphs/frozen_inference_graph.pb', 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    return detection_graph


def inference(image, graph):
    """run inference for single image
    Arguments:
        image -- input numpy array
        graph -- tf.Graph
    Returns:
        output_dict -- outputs
    """
    # Run inference
    output_dict = tf_sess.run(tensor_dict,
                              feed_dict={image_tensor: image})
    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict[
        'detection_classes'][0].astype(np.int64)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    return output_dict


if __name__ == '__main__':
    import cv2
    import numpy as np
    import os
    import glob
    from tqdm import tqdm
    import argparse
    from utils.create_pascalvoc_xml import create_xmldoc, save_xmldoc

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-i', '--input_dir',
                        default="",
                        help="")
    parser.add_argument('-o', '--output_dir',
                        default="",
                        help="")
    args = parser.parse_args()

    # load model and configure output
    detection_graph = load_model()
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with detection_graph.as_default():
        tf_sess = tf.Session(config=tf_config)
        ops = tf.get_default_graph().get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
            'num_detections', 'detection_boxes', 'detection_scores',
            'detection_classes', 'detection_masks'
        ]:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                    tensor_name)
        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

    # loop img dir
    input_dir = args.input_dir
    paths = glob.glob(os.path.join(input_dir, "*.png"))
    for path in tqdm(paths):
        raw_img = cv2.imread(path)
        img = cv2.resize(raw_img, (320, 320))
        img = img[:, :, ::-1]  # convert bgr to rgb
        img = np.expand_dims(img, axis=0)
        # detection
        output_dict = inference(img, detection_graph)

        objects = []
        for i in range(output_dict['num_detections']):
            detection_score = output_dict['detection_scores'][i]
            if detection_score > 0.5:
                # label
                class_id = output_dict['detection_classes'][i]
                if class_id == 1:
                    label = "ball"  # change appropriate label name
                info = []
                info.append(label)

                # bounding box
                h, w, c = raw_img.shape
                box = output_dict['detection_boxes'][i] * np.array(
                    [h, w,  h, w])
                box = box.astype(np.int)
                #x> yv
                info.append(box[1])
                info.append(box[0])
                info.append(box[3])
                info.append(box[2])
                objects.append(info)

        # create xml
        folder = "inputs"
        filename = os.path.basename(path)
        height, width, depth = h, w, c
        doc = create_xmldoc(
            folder, filename, path, height, width, depth, objects)
        # save xml
        output_dir = args.output_dir
        save_xmldoc(doc, os.path.join(
            output_dir, os.path.splitext(filename)[0] + '.xml'))
