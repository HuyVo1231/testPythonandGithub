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
            time.sleep(2)
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
    time.sleep(3)
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
        url = "https://www." + domain + ".com"
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đang được mở.")
        return True
    else:
        return False


# Tìm kiếm trên google.
def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1]
    url = f"https://www.google.com/search?q={search_for}"
    speak("Đang tìm kiếm...")
    webbrowser.open(url)


# Lấy thời gian và giờ hiện tại.
def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôn nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
    else:
        speak("Mình chưa hiểu...")


# Phát youtube
def play_youtube():
    speak("Bạn muốn xem gì trên youtube?")
    my_video = get_text()
    while True:
        result = YoutubeSearch(my_video, max_results=10).to_dict()
        if result:
            break
    url = "https://www.youtube.com" + result[0]["url_suffix"]
    webbrowser.open(url)
    speak("Chúc bạn nghe vui vẻ")


# ffc5594b7ccc13d615d1236fe7babddc
# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
# Xem thời tiết
def weather():
    speak("Bạn muốn xem thời tiết ở nơi nào?")
    url = "https://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "ffc5594b7ccc13d615d1236fe7babddc"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    name = city
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wt = data["weather"]
        weather_des = wt[0]["description"]
        now = datetime.datetime.now()
        content = f""" Hôm nay là ngày {now.day} tháng {now.month} năm {now.year} tại {name}.
          Mặt trời mọc ở vào lúc {sunrise.hour} giờ
        {sunrise.minute} phút. Mặt trời lặn vào lúc {sunset.hour} giờ {sunset.minute} phút. 
        Nhiệt độ trung bình là {current_temp} độ C
        Áp suất không khí là {current_pressure} héc tơ. Độ ẩm {current_humidity}%.
        """
        speak(content)
        time.sleep(25)
    else:
        speak(f"Không tìm thấy {city}")


# gọi trợ lý ảo
def call():
    speak("Xin chào. Bạn tên gì?")
    name = get_text()
    time.sleep(2)
    if name:
        speak("Xin chào {}".format(name))
        time.sleep(2)
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
            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "bài hát" in text:
                play_youtube()
            elif "thời tiết" in text:
                weather()
            elif "dừng" in text or "tạm biệt" in text:
                stop()
                time.sleep(3)
                break


call()
