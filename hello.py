import pyttsx3

import speech_recognition

robot_ear = speech_recognition.Recognizer()
with speech_recognition.Microphone() as mic:
    print("Robot: I'm listening")
    audio = robot_ear.listen(mic)

you = robot_ear.recognize_google(audio, language="vi-VN")
print(you)

robot_brain = you
robot_mouth = pyttsx3.init()
robot_mouth.say(robot_brain)
robot_mouth.runAndWait()
