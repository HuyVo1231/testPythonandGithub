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
wikipedia.set_lang("vi")


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
        url = "https://www." + domain
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


# Xem thời tiết
def weather():
    speak("Bạn muốn xem thời tiết ở nơi nào?")
    url = "https://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "ffc5594b7ccc13d615d1236fe7babddc"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric" + "&lang=vi"
    response = requests.get(call_url)  # Duyệt web ẩn ko cần vào trang web.
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
        Áp suất không khí là {current_pressure} héc tơ. Độ ẩm {current_humidity}%. Ngoài trời đang {weather_des}.
        """
        speak(content)
        time.sleep(28)
    else:
        speak(f"Không tìm thấy {city}")


# Mở ứng dụng
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
    elif "word" in text:
        speak("Mở Microsoft Word")
        os.startfile("C:\Program Files\Microsoft Office\\root\Office16\\WINWORD.EXE")
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile("C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE")
    elif "powerpoint" in text:
        speak("Mở Microsoft Powerpoint")
        os.startfile("C:\Program Files\Microsoft Office\\root\Office16\POWERPNT.EXE")
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")


# Đổi hình nền
# -Qy6jOB9Q_H3CkFMpH1jc28vem8dw00WcItzTQmw3HY -- API KEYS
def change_wallpaper():
    api_key = "-Qy6jOB9Q_H3CkFMpH1jc28vem8dw00WcItzTQmw3HY"
    url = "https://api.unsplash.com/photos/random?client_id=" + api_key
    f = urllib2.urlopen(url)  # Duyệt web không cần giao diện.
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json["urls"]["full"]
    urllib2.urlretrieve(photo, "C:/Users/FPTSHOP/Downloads/image_change.png")
    image = os.path.join("C:/Users/FPTSHOP/Downloads/image_change.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak("Hình nền đã được thay đổi")
    time.sleep(3)


# Đọc định nghĩa trên wiki
def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        text = get_text()
        contents = wikipedia.summary(text).split("\n")
        speak(contents[0])
        time.sleep(20)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            ans = get_text()
            if "có" not in ans:
                break
            speak(content)
            time.sleep(20)
        speak("Cảm ơn bạn đã lắng nghe!!!")
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")


# gửi email
def send_email():
    speak("Bạn gửi email cho ai nhỉ")
    recipient = "hoang yến"
    if "yến" in recipient:
        speak("Nội dung bạn muốn gửi là gì")
        content = "test"
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login("vnhathuy1306@gmail.com", "lfdoatbdgeyfyuxa")
        mail.sendmail(
            "vnhathuy1306@gmail.com", "vonhathuy1306@gmail.com", content.encode("utf-8")
        )
        mail.close()
        speak("Email của bạn vùa được gửi. Bạn check lại email nhé hihi.")
    else:
        speak("Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?")


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
                if "google và tìm kiếm" in text:
                    open_google_and_search(text)
                elif "." in text:
                    open_webiste(text)
                elif "bài hát" in text:
                    play_youtube()
                else:
                    open_application(text)
            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "thời tiết" in text:
                weather()
            elif "hình nền" in text:
                change_wallpaper()
            elif "định nghĩa" in text:
                change_wallpaper()
            elif "email" in text or "gmail" in text or "mail" in text:
                send_email()
            elif "dừng" in text or "tạm biệt" in text:
                stop()
                time.sleep(3)
                break


call()
