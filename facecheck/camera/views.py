from django.shortcuts import render
import numpy as np
import pandas as pd
import cv2
import os
import dlib
import face_recognition
import imutils
from . import fr_align, facealigner_fr, fcong_fr
from .facealigner_fr import FaceAligner_fr
def index(request):
    video = cv2.VideoCapture(0)
    return render(request,'internet/index.html',locals())
def all(request):
    return render(request, 'internet/all.html', locals())
def test(request):
    return render(request, 'internet/test.html', locals())

def name(request):
    global name
    name = request.POST['name']
    if not os.path.isdir('images'):
        os.mkdir('images')
    path = "./images/" + name
    if not os.path.isdir(path):
        os.mkdir('./images/%s' % name)
    return render(request, 'internet/camera.html', locals())

def camera(n):
    value = n
    face_locations = []
    face_encodings = []
    face_encodings_df = pd.DataFrame(columns=["face_encodings"])
    video_capture = cv2.VideoCapture(0)
    while True:
        numbers = value
        if int(numbers) > 0:
            break
    ext = 0
    count = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()  # 實際大小要在 Jetnano 實測

        if ret:
            # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = frame[:, :, ::-1]

            if True:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                if len(face_encodings) > 0:
                    filename = name + '_' + str(ext) + str(hit)
                    face_encodings = face_encodings[0]
                    face_encodings_map = {"face_encodings": face_encodings}
                    face_encodings_df = face_encodings_df.append(face_encodings_map, ignore_index=True)

                    cv2.imwrite("./images/%s/%s.jpg" % (name, filename), frame)
                    ext = ext + 1
                    count = count + 1

            # Display the resulting image
            # cv2.imshow('Video', frame)
        if count == int(numbers):
            break
    # Release handle to the webcam
    # face_encodings_df = face_encodings_df["face_encodings"].values.tolist()
    import csv
    with open("./images/%s/%s_face_features.csv" % (name, filename), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in face_encodings_df["face_encodings"]:
            writer.writerow(row)

    video_capture.release()

def camera1(request):
    ext = request.POST['value']
    camera(ext)
    return render(request, 'internet/test.html', locals())

def only(request):
    title = "上"
    return render(request, 'internet/only.html', locals())
hit = 0

def camera2(request):
    global hit
    if hit == 0:
        camera(1)
        title = "下"
        hit = 1
    elif hit == 1:
        camera(1)
        title = "左"
        hit = 2
    elif hit == 2:
        camera(1)
        title = "右"
        hit = 3
    elif hit == 3:
        camera(1)
        title = "中"
        hit = 4
    elif hit == 4:
        camera(1)
        title = "恭喜您已完成"
        hit = 0
    return render(request, 'internet/step.html', locals())

def camera3(request):
    global hit
    if hit == 0:
        camera(1)
        title = "下"
        hit = 1
    elif hit == 1:
        camera(1)
        title = "左"
        hit = 2
    elif hit == 2:
        camera(1)
        title = "右"
        hit = 3
    elif hit == 3:
        camera(1)
        title = "中"
        hit = 4
    elif hit == 4:
        camera(1)
        title = "恭喜您已完成"
        hit = 0
    return render(request, 'internet/step.html', locals())







