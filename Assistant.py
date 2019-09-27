import pyttsx3
import datetime
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import webbrowser
import wikipedia
import os
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
global stop_words
stop_words = set(stopwords.words("english"))
                 
##critical functionality
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    pass

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"you said: '{query}'\n")
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        return None
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        return None
    return query

##Natural Language Processig stuff goes here
def remove_stop_words(text):
    global stop_words
    words = sent_tokenize(text)
    filtered_sentence = []
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

def parse_query(query):
    query = remove_stop_words(query)
    return ' '.join(query)

##features

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak('Lets save the world together!')

def search_wiki(query):
    speak("Searching wikipedia...")
    query = query.replace('wikipedia', '')
    results = wikipedia.summary(query, sentences = 3)
    speak('wikipedia says...')
    speak(results)

def open_website(query):
    webbrowser.open("youtube.com")

def open_app(query):
    path = switcher.get(app, None)
    if path is None:
        return None
    os.startfile(path)
    
    
def play_music(query):
    music_dir = "D:\\Entertainment and media\\Music\\fab"
    songs = os.listdir(music_dir)
    os.startfile(os.path.join(music_dir, songs[random.randint(0,len(songs)-1)]))
    
def speak_time(query):
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(str_time)

if __name__ == "__main__":
##    speak('Hello Raj, I\'m here to help you make a better world')
    wish()
    switcher = {"wikipedia":"search_wiki(query)",
                "website":"open_website(query)",
                "music":"play_music(query)",
                "time":"speak_time(query)",
                "exit": "exit()"}
    while(True):
        query  = listen()
        if query is not None:
            command = parse_query(query)
            code = switcher.get(command, "speak(\"I'm dumb, I could not catch you\")")
            print(code)
            eval(code)
        
