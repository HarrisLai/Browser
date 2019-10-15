#!/usr/bin/env python
# coding: utf-8

# In[1]:


#使用說明: 記得使用時候必須修改 3個地方 為你的路徑名稱和檔名
# 1. filename = "Harris_" + str(ext)
# 2. cv2.imwrite(".\\images_step-1\\Harris\\%s.jpg" %filename, rgb_small_frame)
# 3. np.savetxt(".\\images_step-1\\Harris\\Harris_face_features.csv", face_encodings_df)


# In[2]:


#提醒注冊使用者 錄影的姿勢和角度盡量滿足在可擷取範圍，
#若是無法辨識為人臉時候處理方式 需再討論


# In[3]:


import numpy as np
import face_recognition
import cv2
import pandas as pd


# In[4]:


video_capture = cv2.VideoCapture(0)


# In[5]:


#此版本會抓取固定數量的 影像特徵數目

import pandas as pd
# Initialize some variables
face_locations = []
face_encodings = []
face_encodings_df = pd.DataFrame(columns=["face_encodings"])

while True:
    numbers = input("請輸入欲儲存的臉部特徵數目(正數)，並請對著鏡頭轉動臉部，當數量到達後鏡頭燈號會自動關閉!(或可透過q鍵提早離開)")
    if int(numbers) > 0:
        break
count = 0
ext = 0
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read() #實際大小要在 Jetnano 實測
    
    if ret:
        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = frame[:, :, ::-1]

        if True:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            if len(face_encodings) > 0:
                filename = "Harris_" + str(ext)
                face_encodings = face_encodings[0]
                face_encodings_map = {"face_encodings":face_encodings}
                face_encodings_df = face_encodings_df.append(face_encodings_map, ignore_index=True)
                print(filename)
                print(ext)
                cv2.imwrite(".\\images_step-1\\Harris\\%s.jpg" %filename, rgb_small_frame)
                ext = ext + 1
                count = count + 1

        # Display the resulting image
        cv2.imshow('Video', frame)
    if count == int(numbers):
        break
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
face_encodings_df = face_encodings_df["face_encodings"].values.tolist()
np.savetxt(".\\images_step-1\\Harris\\Harris_face_features.csv", face_encodings_df)
video_capture.release()
cv2.destroyAllWindows()


# In[6]:


# #此版本會依直抓取特徵直到按下 "q"

# import pandas as pd
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_encodings_df = pd.DataFrame(columns=["face_encodings"])

# while True:
#     # Grab a single frame of video
#     ret, frame = video_capture.read() #實際大小要在 Jetnano 實測
    
#     if ret:
#         # Resize frame of video to 1/4 size for faster face recognition processing
#         #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

#         # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#         rgb_small_frame = frame[:, :, ::-1]

#         if True:
#             # Find all the faces and face encodings in the current frame of video
#             face_locations = face_recognition.face_locations(rgb_small_frame)
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#             if len(face_encodings) > 0:
#                 face_encodings = face_encodings[0]
#                 face_encodings_map = {"face_encodings":face_encodings}
#                 face_encodings_df = face_encodings_df.append(face_encodings_map, ignore_index=True)

#         # Display the resulting image
#         cv2.imshow('Video', frame)

#     # Hit 'q' on the keyboard to quit!
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release handle to the webcam
# face_encodings_df = face_encodings_df["face_encodings"].values.tolist()
# np.savetxt(".\\images_step-1\\Harris\\Harris_face_features.csv", face_encodings_df)
# video_capture.release()
# cv2.destroyAllWindows()


# In[7]:


video_capture.release()
cv2.destroyAllWindows()


# In[ ]:




