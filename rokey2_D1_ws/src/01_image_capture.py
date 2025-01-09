import cv2
import numpy as np
import os 

# 변수 설정 ---①
base_dir = './capture/' # 1 project directory
target_cnt = 400        # 2 수집할 사진 갯수
cnt = 0                 # 사진 촬영 수


dir = os.path.join(base_dir, "aaa")                    ### 3 class directory
if not os.path.exists(dir):
    os.mkdir(dir)

# 카메라 캡쳐 
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        img = frame.copy()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        file_name_path = os.path.join(dir, 'aaa' + str(cnt) + '.jpg')   ### 4 file name prefix
        cv2.imwrite(file_name_path, img)
        cv2.putText(frame, str(cnt), (10, 50), cv2.FONT_HERSHEY_COMPLEX, \
                         1, (0,255,0), 2)
        cnt+=1
        cv2.imshow('face record', frame)
        if cv2.waitKey(1) == 27 or cnt == target_cnt: 
            break
cap.release()
cv2.destroyAllWindows()      
print("Collecting Samples Completed.")