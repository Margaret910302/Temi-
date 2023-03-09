#Course 87
"""import speech_recognition
def listenTo():
    r = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    #轉成文字
    return r.recognize_google(audio,language='zh-TW')
    ##return r.recognize_google(audio,language='en')
#Course 88
import tempfile
from gtts import gTTS
from pygame import mixer
mixer.init()

def speak(sentence):
    with tempfile.NamedTemporaryFile(delete = True) as fp:
        tts = gTTS(text = sentence, lang = 'zh')
        #tts = gTTS(text = sentence, lang = 'zh-HK')
        #tts = gTTS(text = sentence, lang = 'en')
        tts.save("{}.mp3".format(fp.name))
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()
##speak(listenTo())
qa = {
    '今天好嗎':'我很好',
    '今天好帥':'謝謝，你也很漂亮呢!',
    '今天都做了些什麼':'我今天去了文化大學，是個很漂亮的學校呢!',
    'what is the weather today':'The weather today is hot and windy,I suggest you to put on your jacket, when going outside.',
    '請問廁所在哪裡':'向前50公尺再向右轉，就會看到廁所了!'   
}
#按run後要等1秒鐘，再開始問問題
speak(qa.get(listenTo(),'這是新的問題嗎，好的我記下了'))"""

from googletrans import Translator
import speech_recognition as sr
import pyttsx3

# 初始化翻譯器
translator = Translator()
# 初始化語音辨識
r = sr.Recognizer()

# 初始化文字轉語音
engine = pyttsx3.init()
##engine.setProperty('voice','David, Mark')
engine.setProperty('rate',170)

#################
##語音資料庫
qa_dict = {
    '你叫什麼名字': '我是Temi，是個服務型機器人',
    '你今年幾歲了':'我今年四歲了!',
    '今天好嗎':'我很好',
    '今天好帥':'謝謝，你也很漂亮呢!',
    '今天都做了些什麼':'我今天去了文化大學，是個很漂亮的學校呢!',
    'what is the weather today':'The weather today is hot and windy,I suggest you to put on your jacket, when going outside.',
    '請問':'向前50公尺再向右轉，就會看到廁所了!',
    '請問廁所在哪裡':'向前50公尺再向右轉，就會看到廁所了!',
    '請問化妝室在哪裡':'向前50公尺再向右轉，就會看到廁所了!',
    '請問這裡有廁所嗎':'向前50公尺再向右轉，就會看到廁所了!',
    '再見':'下次見!',
}

##分辨使用者問了甚麼問題
def process_question(question):
    if question in qa_dict:
        answer = qa_dict[question]
        print(answer)
        engine.say(answer)
        engine.runAndWait()
    else:
        print('對不起，我不知道答案。')

with sr.Microphone() as source:
    print("Please speak:")
    audio = r.listen(source)
    
    try:
        sentence = r.recognize_google(audio) # 這裡我們使用Google訓練好的語音辨識，Speech Recognition套件中也有其他模型可以用
        print("You said: {}".format(sentence))
        
    except:
        print("Sorry, can't recognize.")
#回答問題
process_question(sentence)  

if translator.translate(sentence).src == 'en':
    translated_sent = translator.translate(sentence, dest='zh-TW').text
    print("Which means {} in Chinese.".format(translator.translate(sentence, dest='zh-TW').text))
    engine.say(translated_sent)
    engine.runAndWait()
else:
    print("This doesn't sound like English")
