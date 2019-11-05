#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 用face_locations取代 detector, _raw_face_landmarks取代predictior

import cv2
import imutils
import dlib
from imutils.face_utils import shape_to_np
# from imutils.face_utils.facealigner import FaceAligner
from imutils import face_utils
import face_recognition
from face_recognition.api import _raw_face_landmarks
import numpy as np
from . import facealigner_fr
from .facealigner_fr import FaceAligner_fr


try:
    import face_recognition_models
except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()

pose_predictor_model = face_recognition_models.pose_predictor_model_location()

predictor = dlib.shape_predictor(pose_predictor_model)
fa = FaceAligner_fr(predictor, desiredFaceWidth=280)

# 輸入參數為某張rgb圖, 原圖人臉位置，number_of_times_to_upsample, model ("hog" or "cnn")
# 會回傳由此圖中被偵測出來而且校正過後的人臉 images (280 x 280) 所組成的 list
ntup = 2
mod = "hog"

def aligned_face_fr(image, f_locations = None, number_of_times_to_upsample=ntup, model = mod):
    
    wd = image.shape[1]

    image = imutils.resize(image, width=800) 

    if f_locations is None:
        flocations = face_recognition.face_locations(image,number_of_times_to_upsample=ntup, model = mod)
    else:
        flocations = []
        for f_ori in f_locations:  # 在原圖的臉位置 
            top = int(f_ori[0]*800/wd)			# 寬調整為800後的臉位置
            right = int(f_ori[1]*800/wd)
            bott = int(f_ori[2]*800/wd)
            left = int(f_ori[3]*800/wd)
            flocations.append((top,right,bott,left))


    raw_landmarks = _raw_face_landmarks(image, flocations, model = "large")
    
    aligned_images_list = []
    for f_l in zip(flocations, raw_landmarks):
        top, right, bott, left = f_l[0]
        rect = [(left,top), (right, bott)]
        (x, y, w, h) = (left, top, right-left, bott - top)
        x1 = max(x,0)
        y1 = max(y,0)
        faceOrig = imutils.resize(image[y1:y + h, x1:x + w], width=256)
        landmk_np = shape_to_np(f_l[1])
        faceAligned_fr = fa.align_fr(image, landmk_np)
        aligned_images_list.append(faceAligned_fr)
    
    return aligned_images_list





