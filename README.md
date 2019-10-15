1.把facecheck載到本地主機  
2.打開view.py更改路徑  
  filename = "你的名稱" + str(ext)   
  cv2.imwrite("存檔路徑\\%s.jpg" %filename, rgb_small_frame)  
  np.savetxt("存檔路徑\Harris_face_features.csv", face_encodings_df)   
3.在facecheck目錄下執行python mange.py runserver  
4.完成
