# Import thư viện trong python và install các thư viện chưa có.
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

# Khai báo ngôn ngữ wiki sẽ tìm là 'vi'
# Khai báo ngôn ngữ là 'vi'

language = "vi"
path = ChromeDriverManager().install()


# Văn bản thành âm thanh
def speak(text):
    print("Trợ lý ảo: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")  # Lưu vào file amthanh.mp3
    playsound.playsound("sound.mp3", False)  # Phát âm file mp3
    os.remove("sound.mp3")  # Remove sau khi phát


# Chuyển âm thanh thành văn bản
def get_audio():
    r = sr.Recognizer()  #  tao Lắng nghe
    with sr.Microphone() as mic:  # Nói vào Mircophone
        print("Tôi: ", end="")
        audio = r.listen(mic, phrase_time_limit=5)  # Đang lắng nghe
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0


# Stop
def stop():
    speak("Hẹn gặp lại sau")


# LChuyển audio thành văn bản
def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(5)
    stop()
    return 0


# Giao tiếp cơ bản
def talk(name):
    day_time = int(strftime("%H"))
    if day_time < 11:
        speak("Chào buổi sáng {} . Chúc bạn một ngày vui vẻ!".format(name))
    elif day_time < 14 and day_time >= 11:
        speak("Chào buổi trưa {} . Chúc bạn buổi trưa vui vẻ!".format(name))
    elif day_time >= 14 and day_time < 17:
        speak("Chào buổi chiều {}. Chúc bạn buổi chiều vui vẻ!".format(name))
    else:
        speak("Chào buổi tối {}. Chúc bạn buổi tối vui vẻ".format(name))
    time.sleep(5)
    speak("Bạn có khỏe không?")
    time.sleep(3)
    ans = get_audio()
    if ans:
        if "có" in ans or "không" not in ans:
            speak("Thật là tốt")
        else:
            speak("Hãy giữ gìn sức khỏe nhé")


# Mở webiste
def open_webiste(text):
    regex = re.search("mở (.+)", text)  # re.search . Lấy tất cả phía sau từ "mở"
    if regex:
        domain = regex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đang được mở.")
        return True
    else:
        return False


def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1]
    url = f"https://www.google.com/search?q={search_for}"
    speak("Đang tìm kiếm...")
    webbrowser.open(url)


open_google_and_search("tìm kiếm sơn tùng")


# gọi trợ lý ảo
def call():
    speak("Xin chào. Bạn tên gì?")
    name = get_text()
    time.sleep(2)
    if name:
        speak("Xin chào {}".format(name))
        time.sleep(3)
        speak("Bạn cần mình làm gì ạ?")
        while True:
            text = get_text()
            if not text:
                break
            elif "trò chuyện" in text or "nói chuyện" in text:
                talk(name)
            elif "mở" in text:
                open_webiste(text)
            elif "tìm" in text:
                open_google_and_search(text)
            elif "dừng" in text or "thôi" in text:
                stop()
                time.sleep(5)
                break


call()
