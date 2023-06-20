import requests
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps

#Load your model
model = load_model("keras_model.h5", compile=False)

#Load your labels
class_names = open("labels.txt", "r").readlines()

#Create the array of the right shape to feed into the keras model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#觸發IFTTT中的Webhooks事件，將跌倒偵測結果傳遞到LINE
def send_ifttt_notification(message):
    event_name = 'fall_detected'
    webhook_key = 'IFTTT_Webhookskey'  #替換為您在IFTTT中獲取的Webhooks金鑰
    url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}'
    data = {'value1': message}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('緊急訊息已發送至LINE')
    else:
        print('無法發送緊急訊息至LINE')

#讀取影片檔案
video_path = 'fall_6.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Cannot open video file")
    exit()

frame_count = 0
fall_count = 0
fall_threshold = 5
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video file")
        break

    frame_count += 1
    if frame_count % 15 != 0: #每15禎取一次偵測
        continue  # Skip frames

    #Resize the frame for faster processing
    frame = cv2.resize(frame, (650, 500))

    #Preprocess the frame for prediction
    image = Image.fromarray(frame).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    #Predict the class and confidence score
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    class_name1 = class_names[index]
    confidence_score = prediction[0][index]

    #Print prediction and confidence score
    print("Class:", class_name1[2:], end="")  #將字串切片後，從第3個字開始看
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Display the prediction on the frame
    cv2.putText(frame, class_name, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, f"Confidence: {confidence_score:.2f}",
                (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('oxxostudio', frame)
    #Check for fall detection
    if class_name1[2:6] == 'fall':
        fall_count += 1
        if fall_count >= fall_threshold:
            #發送郵件
            message = '跌倒偵測到緊急情況！'
            send_ifttt_notification(message)
            fall_count = 0  # Reset fall count
    else:
        fall_count = 0  # Reset fall count if another class is detected

        
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
