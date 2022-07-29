from flask import Flask, render_template
import speech_recognition as sr
from pyfirmata import Arduino, SERVO, util
from time import sleep
import pyaudio

app = Flask(__name__)
# Here You Write your port and pin.
port = "COM3"
pin = 10

board = Arduino(port)
board.digital[pin].mode = SERVO


# moving the board
def move(angle):
    board.digital[pin].write(angle)
    sleep(0.035)


def recognize_language(is_english):
    """
       This Function recognize the voice in different langauge
       based on the is_english bool value.
       it ends the text when  the user stops speaking,
       if the user does not speak or there is any other error it will send a message
    """
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    r.energy_threshold = 300
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Speak Anything .. : ')
        audio = r.listen(source)
        language = 'ar-AR' if not is_english else 'en-US'
        try:
            if r.recognize_google(audio, language=language) == "يسار" or r.recognize_google(audio, language=language) == "left":
                print("Hello")
                for i in range(180, 0, -1):
                    print("rotating back to the left")
                    move(i)
                return "You said to the left"
            elif r.recognize_google(audio, language=language) == "يمين" or r.recognize_google(audio, language=language) == "right":
                for i in range(0, 180):
                    print("rotating to the right")
                    move(i)
                return "You Said to The right"
            else:
                return "I do not Understand"
        except:
            # non-recognizable
            return "Could not Recognize your voice"


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/get-text/<en>")
def get_text(en):
    is_english = True if en == "True" else False
    text = recognize_language(is_english)
    return render_template("index.html", result=text)


if __name__ == '__main__':
    app.run(debug=True)