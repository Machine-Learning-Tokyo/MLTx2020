class Constant(object):
    # Default configs
    API_HOST = '0.0.0.0'
    # API_HOST = '65.49.78.237'
    API_PORT = 8006

    GPU_ID = 0


class FaceDetectionConstant(Constant):
    # Default configs
    GPU_ID = 0

    face_detection_model_path = ''


class AgeGenderConstant(Constant):
    GPU_ID = 0

    age_and_gender_model_path = '/data/compl_runtime_env/face/mobilenet224_1.0_coco_33.h5'



class EmotionConstant(Constant):
    GPU_ID = 0

    emotion_model_path = ''

