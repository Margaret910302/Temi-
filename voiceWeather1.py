import requests
import pyttsx3
import speech_recognition as sr
# 向中央氣象局的 API 發送請求
url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-6AAD2B08-F603-42FC-BEDE-02A90C744196&downloadType=WEB&format=JSON'
data = requests.get(url)   # 取得 JSON 檔案的內容為文字
data_json = data.json()    # 轉換成 JSON 格式
location = data_json['cwbopendata']['dataset']['location']   # 取出 location 的內容
for i in location:
    city = i['locationName']    # 縣市名稱
    wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
    maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
    mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
    ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
    pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
    print(f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %')

# 語音設置
# 麥克風接收語音
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak:")
    audio = r.listen(source)
# 將語音轉為文字
try:
    text = r.recognize_google(audio, language='zh-TW')
    print("You said: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


# 將聽取指定縣市的天氣預報做文字轉語音，再回覆給使用者
# 在使用者指定縣市後，透過語音方式回覆他所想聽到的資訊
for i in location:
    city = i['locationName']    # 縣市名稱
    if city in text:    # 判斷是否有使用者指定的縣市
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
        ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
        pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
        txt = f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %'
        print('Please speak:')
        engine = pyttsx3.init()
        engine.say(txt)
        print(txt)
        engine.runAndWait()
        break
else:
    print("Sorry, the city you specified is not available.")
