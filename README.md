1.把facecheck載到本地主機  
2.安裝python3.6.8以上版本  
3.在命令提示字元cmd打pip install django(安裝django)  
4.在facecheck目錄下執行python mange.py runserver  
5.在命令提示字元facecheck目錄下執行ngrok.exe  
6.將facecheck目錄下的setting.py的 ALLOWED_HOSTS = []更改成  ALLOWED_HOSTS = ['你的ngrok的網頁地址', 'localhost', '127.0.0.1']  
7.依照網頁動作(輸入名稱，特徵擷取數目)    
8.完成
