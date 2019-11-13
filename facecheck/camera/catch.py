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

def camera(request):
    if request.method == 'POST':
        global name
        name = request.POST['name']
        # if not os.path.isdir(name):
        #     os.mkdir(name)
    if request.method == 'GET':
        value = request.GET['value']

        video_capture = cv2.VideoCapture(0)

        while True:
            numbers = value
            if int(numbers) > 0:
                break
        cnnModYN = 1       # 1: 用cnn model    0: 用 hog model        
        f_largeYN =  0      # 1: 要取68點， 0: 要取5點
        alignYN = 1        # 1: 要做校正， 0: 不做校正

        if cnnModYN == 1:
            mod = "cnn"
        elif cnnModYN == 0:
            mod = "hog"

        ext = 0   

        ntup = 2 # number of times to upsample
        # mod = "hog"  # 在jason nano 或 colab上時改成 "cnn"

        encodings = []
        pictures = []

        df_std = pd.DataFrame()
        df = pd.DataFrame()

        foldername = name + "_mod" + str(cnnModYN) + "_lagreface" + str(f_largeYN) + "_alignYN"+str(alignYN)
        if not os.path.isdir(foldername):
            os.mkdir(foldername)

        while True:

            # Grab a single frame of video
            ret, frame = video_capture.read()  # 實際大小要在 Jetnano 實測

            if ret:
                # Resize frame of video to 1/4 size for faster face recognition processing
                # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = frame[:, :, ::-1]
                    # Find all the faces and face encodings in the current frame of video
	                # 先校正
	                # 找出原圖中所有臉的位置  # 要把原圖中有找到的臉框出來(沒做辨識)
                f_locations = face_recognition.face_locations(rgb_small_frame, ntup, mod)
                if len(f_locations) > 0:  # 如果有偵測到臉，校正並計算校正後的特徵 
                    # 取samples時每張frame只取最大的那一張臉
                    f_areas = []
                    for top, right, bot, left in f_locations:
                        area = (right- left)* (bot -top)
                        f_areas.append(area)
                        max_face_idx = f_areas.index(max(f_areas))

                    # 再以這張最大面積的臉來crop出小臉校正圖
                    f_loc = [f_locations[max_face_idx]]

                    if alignYN == 1:  # 要做校正
                        # 每張校正臉圖是 (280, 280, 3)
                        alignedimages = fr_align.aligned_face_fr(rgb_small_frame, f_loc, ntup, mod)
                        # 再計算校正臉圖特徵
                        f_encodings = []
                        for i, aimg in enumerate(alignedimages):
                            flocations = face_recognition.face_locations(aimg, ntup, model = mod)
                            if len(flocations) > 0:  # 如果有偵測到臉，計算特徵; 沒測到臉，就不管它了
                                if f_largeYN == 1: # 用68點算encodings
                                    en = fcong_fr.face_encodings_fr(aimg, flocations)
                                elif f_largeYN == 0: # 用5點算encodings
                                    en = fcong_fr.face_encodings_fr(aimg, flocations, "small")
                                if len(en) > 0:
                                    filename = name + '_' + str(ext) + '_' + str(i) + "_mod" + str(cnnModYN) +\
                                    		 	"_lagreface" + str(f_largeYN) + "_alignYN" + str(alignYN)
                                    encodings.append(list(en[0]))
                                    df_std = df_std.append(pd.DataFrame(en))
                                    # 存下校正小臉圖 和 圖片名稱路徑
                                    pictures.append(".\%s\%s.jpg" % (foldername, filename))
                                    cv2.imwrite(".\%s\%s.jpg" % (foldername, filename), aimg[:, :, ::-1])  # 存小臉圖
                                    ext += 1
                    elif alignYN == 0:  # 不做校正
                        # 不做校正直接算 encodings
                        if f_largeYN == 1: # 用68點算encodings
                            en = fcong_fr.face_encodings_fr(rgb_small_frame, f_loc)
                        elif f_largeYN == 0: # 用5點算encodings
                            en = fcong_fr.face_encodings_fr(rgb_small_frame, f_loc, "small")
                        # 存下原圖(沒畫框的)
                        if len(en) > 0:  
                            filename = name + '_' + str(ext) + '_0' + "_mod" + str(cnnModYN) +\
                                       "_lagreface" + str(f_largeYN) + "_alignYN" + str(alignYN)
                            encodings.append(list(en[0]))
                            df_std = df_std.append(pd.DataFrame(en))
                            # 存下無框原圖 和 圖片名稱路徑
                            pictures.append(".\%s\%s.jpg" % (foldername, filename))
                            cv2.imwrite(".\%s\%s.jpg" % (foldername, filename), frame)  # 存無框原圖
                            ext += 1

                    for (top, right, bottom, left) in f_locations:  # 存畫上人臉框的原圖
                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.imwrite(".\%s\%s_ori.jpg" % (foldername, filename), frame)  # 存原圖 (可和小臉圖做比較)
                    

                # Display the resulting image
                # cv2.imshow('Video', frame)
            if ext == int(numbers):
                break
        # 存下特徵csv檔
        df = pd.DataFrame({"Encoding":encodings,"Picture":pictures})
        df.to_csv(".\%s\%s.csv" % (foldername, name), encoding="utf-8", index=False)
        df_std.to_csv(".\%s\%s_face_features.csv" % (foldername, name), encoding="utf-8", index=False, header = False)


        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    return render(request, 'internet/camera.html', locals())




