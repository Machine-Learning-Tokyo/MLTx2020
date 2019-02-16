import cv2
import os
import requests
import traceback
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from constant import Constant
from controller import face_detector  # , age_gender_predictor, emotion_predictor
# from utils.auth_helper import requires_auth


# controller init
api_face_features = Blueprint('api_face_features', __name__)

@api_face_features.route('', methods=['POST'])
# @requires_auth

def get_image():
    payload = request.json

    try:
        if payload.fname:
            print("payload.fname received")
            file_source = payload.fname

            filename_without_ext, file_extension = os.path.splitext(file_source)
            fpath = filename_without_ext + '.jpg'

        else:
            print("Request should be done with path of the file: fname")
            return 400


        file_exist_status = os.path.exists(fpath)

        if not file_exist_status:
            print ("given file does not exist, please check the file path")
            return 500

        image_source = cv2.imread(fpath)

        if image_source is None:
            print("given image can not be read...")
            return 500

        image_shape = image_source.shape
        start_time = datetime.now()
        no_of_faces, face_bboxes = face_detector.get_face_bboxes(image_source)
        end_time = datetime.now()

        comp_time = end_time - start_time

        result_response = dict()
        info = dict()
        result = dict()

        info['code'] = 00
        info['computationTime'] = comp_time
        info['source'] = im_src

        result['face_bboxes'] = face_bboxes
        result['face_age_gender'] = []
        result['face_emotion'] = []

        result_response['info'] = info
        result_response['result'] = result
        return jsonify(result_response), 200

    except Exception:
        print("Error")

