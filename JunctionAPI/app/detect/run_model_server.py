# import the necessary packages
# from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
from keras.models import load_model
from app.model import emo_model, age_model
import numpy as np
import time
import cv2
from PIL import Image
import os
import cv2
import tensorflow as tf

# Initialize Global Variable
emo_mdl = None
gender_mdl = None
age_mdl = None
graph = None


args = {'prototxt': "deploy.prototxt.txt",
        'face_model': "res10_300x300_ssd_iter_140000.caffemodel",
        'emo_model': "emo_model.h5",
        'gender_model': "gender_detection.model",
        'age_model': "age_only_resnet50_weights.061-3.300-4.410.hdf5",
        'confidence': 0.5}

def pre_load_model():
	global emo_mdl
	global gender_mdl
	global age_mdl
	global net
	global graph

	# load the Keras Model
	emo_mdl = emo_model.build()
	emo_mdl.load_weights(os.path.join(os.getcwd(),'app', 'weights', args["emo_model"]))
	gender_mdl = load_model(os.path.join(os.getcwd(),'app', 'weights', args["gender_model"]))
	age_mdl = age_model.get_model(model_name="ResNet50")
	age_mdl.load_weights(os.path.join(os.getcwd(), 'app', 'weights', args["age_model"]))
	net = cv2.dnn.readNetFromCaffe(
		os.path.join(os.path.join(os.getcwd(), 'app', 'weights', args['prototxt'])),
		os.path.join(os.path.join(os.getcwd(),'app','weights', args['face_model']))
	)
	graph = tf.get_default_graph()
