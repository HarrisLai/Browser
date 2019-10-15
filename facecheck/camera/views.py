from django.shortcuts import render
import numpy as np
import face_recognition
import cv2
import pandas as pd


# Create your views here.
def index(request):
    if request.method == "POST":
        face_locations = []
        face_encodings = []
        face_encodings_df = pd.DataFrame(columns=["face_encodings"])        
        video_capture = cv2.VideoCapture(0)
        value = request.POST['value']
        while True:
            numbers = value
            if int(numbers) > 0:
                break
        count = 0
        ext = 0
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
                        filename = "Harris_" + str(ext)
                        face_encodings = face_encodings[0]
                        face_encodings_map = {"face_encodings": face_encodings}
                        face_encodings_df = face_encodings_df.append(face_encodings_map, ignore_index=True)
                        print(filename)
                        print(ext)
                        cv2.imwrite(".\\images_step-1\\Harris\\%s.jpg" % filename, rgb_small_frame)
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

        video_capture.release()
        cv2.destroyAllWindows()
    return render(request,'internet/index.html',locals())




