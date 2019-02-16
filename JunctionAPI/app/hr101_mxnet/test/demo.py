from MLT.core.face_detector import TinyFaces
import cv2
import pdb

tinyFaces = TinyFaces()

fname = './img1.jpg'
txtpath = './detections.txt'

number_of_faces, face_bboxes, elapsed_time = tinyFaces.detect(fname, txtpath)
print("Number of detected faces: {}".format(number_of_faces))
print("Detection took: {} secs".format(elapsed_time))



number_of_faces, face_bboxes, elapsed_time = tinyFaces.detect(fname, txtpath)
print("Number of detected faces: {}".format(number_of_faces))
print("Detection took: {} secs".format(elapsed_time))
# for face_bbox in face_bboxes:
#     x1 = face_bbox[0]
#     y1 = face_bbox[1]
#     x2 = face_bbox[2]
#     y2 = face_bbox[3]
#
#     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# cv2.imwrite(fname.replace('.jpg', '_detection.jpg'), img)