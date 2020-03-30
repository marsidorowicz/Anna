import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

print ("Starting Anna")
MASTER = "Mario"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Ta funkcja czyta zadany tekst
def speak(text):
    engine.say(text)
    engine.runAndWait()
#Ustalanie powitania w zależności od pory dnia
def Greeting():
    godzina = int(datetime.datetime.now().hour)

    if godzina>=0 and godzina < 12:
        speak("Good morning "+ MASTER)
    elif godzina>=12 and godzina <21:
        speak("Good afternoon "+ MASTER)
    else: 
        speak("Good evening"+ MASTER)

def przyjmijRozkaz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("How may I assist? ")
        speak("How may I assist?")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = r.recognize_google(audio, language = 'en')
        print(f"user said: {query}\n")
    except Exception as e:
        print("Repeat please")
        speak("repeat please")
        przyjmijRozkaz()
    return query
# Uruchamianie        
#speak("Starting Anna...")
#Greeting()


def main():
     
    query = przyjmijRozkaz()



    if 'wikipedia' in query.lower():
        wikipedia.set_lang("en")
        speak('Searching in wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences =2)
        print(results)
        speak(results)
        main()
    elif 'open youtube' in query.lower():
        webbrowser.get('windows-default').open('http://www.youtube.com')
        main()
    elif 'open google' in query.lower():
        webbrowser.get('windows-default').open('http://www.google.com')
        main()
    elif 'play music' in query.lower():
        speak("Serching for music")
        try:
            f = open("songs.txt", "r")
            if f.mode == "r":
                songs_dir = f.read()
                speak("Songs found in")
                print(songs_dir)
                speak("Playing music")
                songs = os.listdir(songs_dir)
                os.startfile(os.path.join(songs_dir, songs[0]))
                f.close()
                main()
            else:
                speak("Something wrong with the file")
                speak("setting file to read mode")
                f = open("songs.txt", "r")
                main()
        except IOError:
            speak("File was not found. Do you want to show directory with your Music?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                print("Recognizing...")
                speak("Recognizing...")
                query = r.recognize_google(audio, language = 'en')
                print(f"user said: {query}\n")
            except Exception as e:
                print("Repeat")
                speak("repeat please")
        if 'yes' in query.lower():
            speak("Where is music?")
            songs_dir = input("Where is music? ")
            f = open("songs.txt", "w")
            f.write(songs_dir)
            f.close()
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))
            main()
        if 'no' in query.lower():
                main()
        else:
            main()
    elif 'goodbye' in query.lower():
        speak("Goodbye "+MASTER)
    elif 'time' in query.lower():
        time = datetime.datetime.now().strftime("%H:%M")
        print("It is now " + time)
        speak( "It is now " + time)
        main()
    else:
        speak("Goodbye "+MASTER)
    
main()
