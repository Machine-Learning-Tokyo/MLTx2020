import time
import cv2
from ..hr101_mxnet.tiny_fd import TinyFacesDetector

tiny_faces = None

def load_model():
    global tiny_faces
    tiny_faces = TinyFacesDetector(model_root='/home/paperspace/Desktop/Junction/api/app/hr101_mxnet/',
                                    prob_thresh=0.5, gpu_idx=0)


# def detect(fname, txtfname):
#     img = cv2.imread(fname)
#     tic = time.time()
#     boxes = self.detector.detect(self.img)
#     toc = time.time()
#     elapsed_time = toc - tic
#
#     self.write_to_txt_file(fname, boxes, txtfname)
#
#     return boxes.shape[0], boxes, elapsed_time

def get_face_bboxes(img):
    boxes = tiny_faces.detect(img)
    return boxes.shape[0], boxes


def write_to_txt_file(fname, boxes, txtfname):
    txtfile = open(txtfname, 'w')
    txtfile.write(fname + '\n')
    txtfile.write(str(boxes.shape[0]) + '\n')
    for box in boxes:
        line = ''

        x1 = min(max(0, int(box[0])), img.shape[0])
        y1 = min(max(0, int(box[1])), img.shape[1])
        x2 = min(max(0, int(box[2])), img.shape[0])
        y2 = min(max(0, int(box[3])), img.shape[1])
        line += str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n'

        txtfile.write(line)