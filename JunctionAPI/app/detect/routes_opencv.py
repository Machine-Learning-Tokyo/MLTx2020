from flask import redirect, url_for, request, render_template, flash, session
from flask import current_app as current_app
from PIL import Image
import cv2
from app.detect import bp
from app.detect import run_model_server
import numpy as np
from app.detect.forms import DetectForm
from keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt
import os
import io
import imutils
import csv
import sys
sys.path.append('/home/paperspace/Desktop/MLT/Tiny_Faces_in_Tensorflow')
from tiny_face_det import get_img_path
#import tiny_face_eval

@bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if "processed_data" not in session:
        session["processed_data"] = {}
    bucket = session["processed_data"]
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    gender_dict = {0: 'man', 1:'woman'}

    # For data analysis
    emo_count = {"Angry":0, "Disgusted":0, "Fearful":0, "Happy":0, "Neutral":0,
    "Sad":0, "Surprised":0}
    gender_count = {"man":0, "woman":0}
    age_class = {}

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
            image = f.read()
            image = Image.open(io.BytesIO(image)).convert('RGB')
            opencv_img = np.array(image)
            opencv_img = opencv_img[:, :, ::-1].copy()
            age_img_size = run_model_server.age_mdl.input.shape.as_list()[1]
            frame = imutils.resize(opencv_img, width=400)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
            # pass the blob through the network and obtain the detections and
            # predictions
            run_model_server.net.setInput(blob)
            detections = run_model_server.net.forward()
            print(detections)
            #img_path = '/home/paperspace/img.jpg'
            #cv2.imwrite(img_path, frame)
            #detections = get_img_path(img_path)
            count = 0

            history_data = []
            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < 0.5:
                    continue
                count += 1
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Extract the patches
                img_patch = frame[startY:startY + (endY-startY), startX:startX + (endX - startX)]

                # Patch for Emo detect
                emo_patch = cv2.cvtColor(img_patch, cv2.COLOR_RGB2GRAY)
                emo_patch = np.expand_dims(np.expand_dims(cv2.resize(
                    emo_patch, (48, 48)), -1), 0)

                # Patch for gender detect
                gender_patch = cv2.resize(img_patch, (96, 96))
                gender_patch = gender_patch.astype("float") / 255.0
                gender_patch = img_to_array(gender_patch)
                gender_patch = np.expand_dims(gender_patch, axis=0)

                # Path for age detect
                age_patch = cv2.cvtColor(img_patch, cv2.COLOR_BGR2RGB)
                age_patch = cv2.resize(age_patch, (age_img_size, age_img_size))
                age_patch = np.expand_dims(age_patch, axis=0)

                graph = run_model_server.graph
                with graph.as_default():
                    predicted_age = run_model_server.age_mdl.predict(age_patch)
                    ages = np.arange(0, 101).reshape(101, 1)
                    predicted_age = int(predicted_age.dot(ages).flatten())

                    detected_gender = run_model_server.gender_mdl.predict(gender_patch)[0]
                    gender_index = int(np.argmax(detected_gender))

                    predicted_emo = run_model_server.emo_mdl.predict(emo_patch)

                    emo_index = int(np.argmax(predicted_emo))
                    emo_count[emotion_dict[emo_index]] += 1
                    gender_count[gender_dict[gender_index]] += 1
                    if str(predicted_age) in age_class:
                        age_class[str(predicted_age)] +=1
                    else:
                        age_class[str(predicted_age)] = 1
                    history_data.append([emotion_dict[emo_index],gender_dict[gender_index],predicted_age,(startX,startY, endX, endY)])

                # draw the bounding box of the face along with the associated
                # probability
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 0), 2)

            static_file_path = os.path.join(os.getcwd(), "app", "static")
            # Generate Emotion Status
            xs = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']
            ys = []
            data = emo_count
            ys = [data['Angry'], data['Disgusted'], data['Fearful'], data['Happy'], data['Neutral'], data['Sad'], data['Surprised']      
            plt.bar(list(xs), ys, align='center', alpha=0.5)

            plt.ylabel('Number of people')
            plt.title('Emotion Classification')
            plt.savefig(os.path.join(static_file_path,'emotion_status.png'))
            plt.cla()

            # Generate Gender Count
            xs = ['MAN', 'WOMAN']
            ys = []
            data = gender_count
            ys = [data['man'], data['woman']]
            plt.bar(list(xs), ys, align='center', alpha=0.5)

            plt.ylabel('Number of people')
            plt.title('Gender Classification')
            plt.savefig(os.path.join(static_file_path,'gender_status.png'))
            plt.cla()

            # Age Classification
            data = age_class
            xs = []
            ys = []
            for item, lst in data.items():
                xs.append(item)
                ys.append(data[item])
            plt.plot(list(xs), ys, label='Crowd Count', color='blue')
            plt.title("Age Classification Status")
            plt.xlabel("Age")
            plt.ylabel("Number of people")
            plt.legend(loc='upper right')
            plt.savefig(os.path.join(static_file_path,'age_status.png'))

            file_name = "{}_detect.{}".format(f.filename.split('.')[0],f.filename.split('.')[1])
            cv2.imwrite(os.path.join(static_file_path, file_name), frame)
            # Note we must return 200 HTTP OK response.
            # Saving csv for historical data analysis.
            # TODO: Change to database.
            with open(os.path.join(os.getcwd(),'app', 'records', 'camera1.csv'), mode='a') as data_file:
                data_file= csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(len(history_data)):
                    data_file.writerow(list(history_data[i]))

            bucket['file_name'] = file_name
            bucket['detected_person'] = count
            session['processed_data'] = bucket
            return "Successfully processed.", 200
    else:
        return render_template('detect/../templates/detect/upload.html', title="Tokyo Junction",
                               form=form)

@bp.route('/result')
def result():
    if "processed_data" not in session:
        return redirect(url_for('detect.detect'))
    processed_data = session["processed_data"]
    file_name = processed_data['file_name']
    person_count = processed_data['detected_person']
    session.pop('processed_data', None)
    # TO DO
    # Display the processed data on the page
    print("Here result")
    return render_template('detect/../templates/detect/results.html', file_name=file_name, people_count=person_count)

@bp.route('/public')
def public():
    print("Public...")
    return render_template('detect/../templates/detect/public.html')
