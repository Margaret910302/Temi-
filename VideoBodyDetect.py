import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
#"D:\\falls_dectection\\video\\fall_detection_3.mp4" 影片路徑
video_path = "YourVideo.mp4"  # 指定你的動態影片路徑

cap = cv2.VideoCapture(video_path)  # 使用指定路徑的動態影片

with mp_pose.Pose( #辨識率參數(0~1，數字越小越不嚴謹，越大反之)
    min_detection_confidence=0.8,       #原本0.5
    min_tracking_confidence=0.8) as pose: #原本0.5

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        img = cv2.resize(img, (520, 300))
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img2)

        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
