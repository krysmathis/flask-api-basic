from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import shutil
import requests
import math

from collections import defaultdict
from io import StringIO
from PIL import Image

from machine.object_detection.utils import ops as utils_ops
from machine.object_detection.utils import label_map_util
from machine.object_detection.utils import visualization_utils as vis_util

class Detector(Resource):
    
    __detection = []
    __url = ''
    __prediction_url = ''

    def detection(self):
        return self.__detection

    def url(self):
        return self.__prediction_url

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def download_image(self, url):
        file_len = len([file for file in os.listdir('static/images') if file[-4:] == ".jpg"])
        response = requests.get(url, stream=True)
        filename = os.path.join('static/images','image{}.jpg'.format(file_len+1))
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return filename

    def run_inference_for_single_image(self,image, graph):
        with graph.as_default():
            with tf.Session() as sess:
            # Get handles to input and output tensors
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
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                        feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]
            return output_dict


    
    def detect(self):
        # What model to download. This is the folder with the model.
        MODEL_NAME = 'frozen_graph'

        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        PATH_TO_CKPT = 'machine/' + MODEL_NAME + '/frozen_inference_graph.pb'

        # List of the strings that is used to add correct label for each box.
        PATH_TO_LABELS = os.path.join('machine/data', 'object-detection.pbtxt')

        NUM_CLASSES = 2

        PATH_TO_TEST_IMAGES_DIR = 'test_images'

        PATH_TO_TEST_IMAGES_DIR = '/Users/krystopher/Dropbox/Apps/shelf-api'
        # variable to hold the number of images in the test_images directory
        file_len = len([file for file in os.listdir(PATH_TO_TEST_IMAGES_DIR) if file[-4:] == ".jpg"])
        print(file_len)
        #TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(math.ceil(file_len/2), file_len) ]
        #TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format('21'))]
        TEST_IMAGE_PATHS = []
        DOWNLOAD_PATH = self.download_image(self.__url)

        TEST_IMAGE_PATHS.append(DOWNLOAD_PATH)
        # Size, in inches, of the output images.
        IMAGE_SIZE = (12, 8)

        # load the frozen detection graph into memory
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        for image_path in TEST_IMAGE_PATHS:
            print('image_path: ', image_path)
            image = Image.open(image_path)
            # print("origial image size: ", image.size)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = self.load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            output_dict = self.run_inference_for_single_image(image_np, detection_graph)

            # print(category_index)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8)
            # print(instance_masks)
        #     plt.figure(figsize=IMAGE_SIZE)
            
            # Saving the image
            #IMAGE_SAVE_PATH = os.path.join(PATH_TO_TEST_IMAGES_DIR,'image_prediction.jpg')
            IMAGE_SAVE_PATH = image_path.replace('.jpg','_prediction.jpg')
            self.__prediction_url = IMAGE_SAVE_PATH
            im = Image.fromarray(image_np)
            im.save(IMAGE_SAVE_PATH)

            detections = [output_dict['detection_classes'][idx] for idx, v in enumerate(list(output_dict['detection_scores'])) if v > .8]
            self.__detection = [category_index[v]['name'] for v in detections]

    def __init__(self, url):
        self.__url = url
        self.detect()