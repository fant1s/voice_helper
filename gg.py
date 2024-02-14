import os 
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import requests
import webbrowser

opts = {
    "alias": ('гидеон', 'гедеон', 'гидон', 'гедон', 'джарвис', 'привет', 'компуктер', 'включи' ,'компьютер', 'открой'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'реши', "помоги"),
    "cmds": {
        "shotdown": ('выключи ноутбук', 'выключи комп'),
        "browser": ("зайди в гугл", "зайди в интернет"),
        "games": ('включи игру', "хочу поиграть"),
        'fortnite': ('fortnite'), 
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку','хочу музыку', 'включи радио'),
        "stupid1": ('Раскажи анекдот', 'расмеши меня', 'ты знаешь анекдоты'),
        'search': ('найди мне'),
        'tg': ('телеграмм', 'telegram')
    }
}



#функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

speak_engine = pyttsx3.init()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
           
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def search_google(query):
    query = voice
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)


def execute_cmd(cmd):
    if cmd == 'search':
        speak('Эта функия пока в разработке')
        return execute_cmd
    if cmd == "shotdown":
        os.system("shutdown -s")
        return execute_cmd
    if cmd == 'tg':
        telega = 'Telegram.lnk'
        os.system(telega)
    if cmd == 'fortnite':
        fortnite = 'Fortnite.url'
        os.system(fortnite)
    if cmd == 'browser':
        chrome = "C:\player\Google.lnk"
        os.system(chrome)
        return execute_cmd
    if cmd == 'ctime':
        # Тек.время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
        return execute_cmd
        # музло
    elif cmd == 'radio':
        path = "C:\player\dist\main\main.exe"
        os.system(path)
        return execute_cmd
        # анекдоты 
    elif cmd == 'stupid1':
      speak("Мой разработчик не научил меня анектодам.... ХА ХАХА")
      return execute_cmd
    else:
      print('Команда не распознана')

#запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 0)

with m as source:
   r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

voice = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voice[0].id)

speak('Добрый день')
speak('Голосовой помощник к вашим услугам')
speak("К сожелению некотрые функции не работают")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0)