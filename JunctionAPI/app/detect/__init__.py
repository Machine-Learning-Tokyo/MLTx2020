from flask import Blueprint

bp = Blueprint('detect', __name__)

from app.detect import routes

# from Junction.api.app.detect.face_detector import FaceDetector
# from app.core import FaceDetector

from app.detect import face_detector

face_detector.load_model()

# from app.detect.face_detector import FaceDetector
# face_detector_object = FaceDetector()

