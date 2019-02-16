from flask import redirect, url_for, request, render_template, flash, session
from flask import current_app as current_app
from PIL import Image
import numpy as np
import pdb

from app.detect import face_detector

import cv2
from app.detect import bp

from app.detect.forms import DetectForm
import os
import io


@bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if "processed_data" not in session:
        # To store the processed_data
        session["processed_data"]  = {}
    form = DetectForm()
    current_app.config.update(DROPZONE_UPLOAD_ON_CLICK=True)
    # if request.method == 'GET':
    #     print("Here visited")
    #     return render_template('detect/upload.html', title="Upload Files")
    # else:
    #     print("Posted Done")
    #     return "Successfully processed.", 200
    if request.method == "POST":
        for (key, f) in (request.files.items()):
            # f.save(os.path.join(os.getcwd(),"app","uploads", f.filename))
            print("Got the file {}".format(f.filename))
            image = f.read()
            image = Image.open(io.BytesIO(image)).convert('RGB')
            opencv_img = np.array(image)
            opencv_img = opencv_img[:, :, ::-1].copy()

            number_of_faces, bboxes = face_detector.get_face_bboxes(opencv_img)

            for box in bboxes:
                x1 = box[0]
                y1 = box[1]
                x2 = box[2]
                y2 = box[3]
                cv2.rectangle(opencv_img, (x1,y1), (x2, y2), (0, 0, 255), 2)

                patch = opencv_img[y1:y2, x1:x2]
            cv2.imwrite('/home/paperspace/Desktop/patch.jpg', patch)
            cv2.imwrite(os.path.join(os.getcwd(),"app","uploads", f.filename.replace('.jpg', '_detection.jpg')), opencv_img)

            print(number_of_faces)
            # Starting your work here...

            # Note we must return 200 HTTP OK response.
            return "Successfully processed.", 200
    else:
        return render_template('detect/upload.html', title="Tokyo Junction",
        form=form)

@bp.route('/result')
def result():
    if "processed_data" not in session:
        return redirect(url_for('detect.detect'))
    processed_data = session["processed_data"]
    session.pop('processed_data', None)
    # TO DO
    # Display the processed data on the page
    print("Here result")
    return render_template('detect/results.html')
