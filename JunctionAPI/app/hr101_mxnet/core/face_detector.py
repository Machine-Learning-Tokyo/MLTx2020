import time
import cv2


class FaceDetector():
    def __init__(self):
        from tiny_fd import TinyFacesDetector
        self.tiny_faces = TinyFacesDetector(model_root='./', prob_thresh=0.5, gpu_idx=0)

    def detect(self, fname, txtfname):
        self.img = cv2.imread(fname)
        tic = time.time()
        boxes = self.detector.detect(self.img)
        toc = time.time()
        elapsed_time = toc - tic

        self.write_to_txt_file(fname, boxes, txtfname)

        return boxes.shape[0], boxes, elapsed_time

    def get_face_bboxes(self, img):
        boxes = self.tiny_faces.detect(self.img)
        # return boxes.shape[0], boxes
        return 127, [1,2,3,4]
    def write_to_txt_file(self, fname, boxes, txtfname):
        txtfile = open(txtfname, 'w')
        txtfile.write(fname + '\n')
        txtfile.write(str(boxes.shape[0]) + '\n')
        for box in boxes:
            line = ''

            x1 = min(max(0, int(box[0])), self.img.shape[0])
            y1 = min(max(0, int(box[1])), self.img.shape[1])
            x2 = min(max(0, int(box[2])), self.img.shape[0])
            y2 = min(max(0, int(box[3])), self.img.shape[1])
            line += str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n'

            txtfile.write(line)