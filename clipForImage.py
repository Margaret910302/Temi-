import cv2
import math

cap = cv2.VideoCapture('video//yourVideo.mp4')
frameRate = cap.get(5) #frame rate, every 5 frame 
print(frameRate)
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    print(frameId)
    ret, frame = cap.read()
    if (ret != True):
        break
    #if (frameId % math.floor(frameRate) == 0):
    if (frameId % math.floor(5) == 0):
        filename = "image_" +  str(int(frameId)) + ".jpg"
        filename = "imgs//" + filename
        cv2.imwrite(filename, frame)
cap.release()
print("Done!")
