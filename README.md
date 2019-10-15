1.把facecheck載到本地主機  
2.打開view.py更改路徑  
  filename = "Harris_" + str(ext)   
  cv2.imwrite(".\\images_step-1\\Harris\\%s.jpg" %filename, rgb_small_frame)  
  np.savetxt(".\\images_step-1\\Harris\\Harris_face_features.csv", face_encodings_df)   
3.在facecheck目錄下執行python mange.py runserver  
4.完成
