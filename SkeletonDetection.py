import cv2
import time
import mediapipe

mp_drawing = mediapipe.solutions.drawing_utils         #繪圖方法
mp_drawing_styles = mediapipe.solutions.drawing_styles #繪圖樣式
mp_holistic = mediapipe.solutions.holistic             #全身偵測方法
mp_pose = mediapipe.solutions.pose                     #人體姿勢估計模型
pose = mp_pose.Pose()

#cap = cv2.VideoCapture(0)  #使用鏡頭
cap = cv2.VideoCapture('江八點健身操1.mp4')

times = 0

file = open("江八點Information.txt", "w", encoding='utf-8')

with mp_holistic.Holistic(     #啟用偵測全身
    min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    if not cap.isOpened():
        print("無法開啟攝影機")
        exit()
    while True:
        ret, img = cap.read()
        if not ret:
            print("無法擷取影像")
            break
        if ret:
            img = cv2.resize(img, (1040, 600))            # 修改圖片大小
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將BGR轉換成RGB
            results = holistic.process(img2)              # 開始偵測

            mp_drawing.draw_landmarks(   #臉部網格
                img,
                results.face_landmarks,
                mp_holistic.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())

            mp_drawing.draw_landmarks(   #身體骨架
                img,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style())

            print('第 ', times, " 幀", file = file)
            times += 1

            # 使用人體姿勢估計模型
            results2 = pose.process(img)

            if results2.pose_landmarks is not None: # 有檢測到座標點
                pose_landmarks = results2.pose_landmarks.landmark

                # 取得33個點的座標
                landmarks = results2.pose_landmarks.landmark

                landmarkLabel = 0
                for landmark in landmarks:
                    x = landmark.x
                    y = landmark.y
                    z = landmark.z
                    print('標籤:', landmarkLabel, 'x軸:', x, 'y軸:', y, 'z軸:', z, file = file)
                    landmarkLabel += 1
            else:
                print('沒有偵測到')
                continue

            # imgFlip = cv2.flip(img, 1)  左右水平翻轉
            cv2.imshow('Body Detection', img)
        else:
            break
        key = cv2.waitKey(5)
        if key == ord('q') or key == 27 or key == 13 or key == ord(' '):
            break  # 按下 q 鍵     27==esc鍵     13==enter鍵 停止     ord('字元')=>將字符轉化為對應的整數(ASCII碼)
        
file.close()
cap.release()            #釋放WebCam
cv2.destroyAllWindows()  #關閉視窗
