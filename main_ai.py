# My Jarvis project to control the my laptop/PC through my voice

import keyboard
import subprocess as sp
import imdb
import mtranslate
import pyautogui
import webbrowser
import time
import os
from datetime import datetime
import sys
from decouple import config
import pyttsx3
from random import choice, random
from const import random_text
from online import search_on_google, search_on_wikipedia, send_email, youtube, get_news, weather_forecast
import pywhatkit, datetime, requests, wikipedia, pyjokes
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
import speech_recognition as sr
from jarvis_main_gui_file import Ui_jarvis_main_gui
from PyQt5.QtCore import QThread
from plyer import notification
from PyQt5.QtWidgets import QApplication, QMainWindow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty("rate", 150)

USER = config('SIR')
HOSTNAME = config('Jarvis')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    ui.updateMovieDynamically("speaking")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        ui.terminalPrint("--------------------------------------Jarvis: Good Morning Sir---------------------------------------- ")
        speak(f"Good morning sir")
    elif hour >= 12 and hour < 17:
        ui.terminalPrint("Jarvis: Good Afternoon Sir")
        speak(f"Good afternoon sir")
    elif hour >= 17 and hour < 21:
        ui.terminalPrint("Jarvis: Good Evening Sir")
        speak(f"Good evening sir")
    else:
        ui.terminalPrint("Jarvis: Good Night Sir")
        speak("Good Night Sir")
    ui.terminalPrint(
        f"        -----------------------I am {HOSTNAME}. How may i assist you? {USER}-----------------------\n")
    speak(f"I am {HOSTNAME}. How may i assist you {USER}?")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening ")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


class jarvisMainClass(QThread):
    def __init__(self):
        super(jarvisMainClass, self).__init__()

    def run(self):
        self.runJarvis()

    def take_command(self):
        cmd = " "
        while cmd == " ":
            ui.updateMovieDynamically("listening")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                ui.updateMovieDynamically("loading")
                ui.terminalPrint("Wait for few Moments..\n")
                cmd = r.recognize_google(audio, language='en-in')
                cmd = mtranslate.translate(cmd, to_language="en-in")
                ui.terminalPrint(f"You just said: {cmd}\n")

                if not 'stop' in cmd or 'exit' in cmd:
                    # speak(choice(random_text))
                    pass
                else:
                    hour = datetime.now().hour
                    if hour >= 21 and hour < 6:
                        speak("Good night sir,take care!")
                    else:
                        speak("Have a good day sir!")
                    exit()

            except Exception:
                ui.terminalPrint("Sorry I couldn't understand. Can you please repeat that?")
                speak("Sorry I couldn't understand. Can you please repeat that?")

            # return cmd
        return cmd

    def runJarvis(self):
        greet_me()
        running = True
        while running:
            if listening:
                query = self.take_command().lower()
                if 'time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"Sir the time is {strTime}")
                    ui.terminalPrint(strTime)
                elif ("hello" in query) or ("hey" in query) or ("hi" in query) or ("good morninig" in query) or (
                        "good afternoon" in query) or ("good evening" in query):
                    ui.terminalPrint("-----welcome Boss what do you want--------")
                    speak("welcome Boss what do you want")
                elif "thank you" in query:
                    ui.terminalPrint("you welcome Boss")
                    speak("you welcome Boss")
                elif "open command prompt" in query:
                    ui.terminalPrint("Opening command prompt sir")
                    speak("Opening command prompt")
                    os.system('start cmd')
                elif "open camera" in query:
                    ui.terminalPrint("Opening camera sir")
                    speak("Opening camera sir")
                    sp.run('start microsoft.windows.camera:', shell=True)
                elif "play song" in query:
                    ui.terminalPrint("I play the song from the URL you have given me Boss.")
                    speak("I play the song from the URL you have given me Boss.")
                    webbrowser.open(choice(random_text))
                elif "open youtube" in query:
                    ui.terminalPrint(f"What do you want to search on YouTube {USER} ?")
                    speak("What do you want to play on youtube sir ?")
                    video = self.take_command().lower()
                    ui.terminalPrint(f"I am searching {USER}: {video}")
                    youtube(video)
                elif "open google" in query:
                    speak(f"What do you want to search on google {USER} ?")
                    ui.terminalPrint(f"What do you want to search on google {USER} ?")
                    query = self.take_command().lower()
                    ui.terminalPrint(f"I am searching {USER}: {query}")
                    search_on_google(query)
                elif "wikipedia" in query:
                    ui.terminalPrint("what do you want to search on wikipedia sir?")
                    speak("what do you want to search on wikipedia sir?")
                    search = self.take_command().lower()
                    results = search_on_wikipedia(search)
                    speak(f" I am searching sir : {search}")
                    ui.terminalPrint(f"According to wikipedia:->\n,{results}")
                    speak(f"According to wikipedia,{results}")

                elif 'open' in query:
                    speak("I am opening sir...")
                    query = query.replace("open", "")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                elif ("send email" in query) or ("send mail" in query):
                    from send_email import send_emails
                    speak("On what email address do you want to send sir?. Please enter in the terminal")
                    receiver_add = input("enter email:")
                    ui.terminalPrint(receiver_add)
                    speak("What should be the subject sir?")
                    subject = self.take_command().capitalize()
                    ui.terminalPrint(subject)
                    speak("What should be the title sir?")
                    titles = self.take_command().capitalize()
                    ui.terminalPrint(titles)
                    speak("What is the message ?")
                    message = self.take_command().capitalize()
                    temp = f"Dear {titles},\n\n{message}\n\nThanks & Regard\n Gopi Nishad\n"
                    if send_emails(receiver_add, subject, temp):
                        speak("I have sent the email sir")
                        ui.terminalPrint("I have sent the email sir")
                    else:
                        speak("something went wrong Please check the error log")
                elif 'weather' in query:
                    speak("tell me the name of your city")
                    text = self.take_command()
                    # city =input("Enter name of your city")
                    speak(f"Getting weather report for your city {text}")
                    weather, temp, feels_like = weather_forecast(text)
                    speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    ui.terminalPrint(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")
                elif "movie" in query:
                    movies_db = imdb.IMDb()
                    speak("Please tell me the movie name:")
                    ui.terminalPrint("Please tell me the movie name:")
                    text = self.take_command()
                    movies = movies_db.search_movie(text)
                    speak("Searching for " + text)
                    ui.terminalPrint("Searching for " + text + "\n")
                    speak("I found these movies:")
                    ui.terminalPrint("I found these movies:\n")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        ui.terminalPrint(f"{title} - {year}")
                        speak(f"{title} - {year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info.get("rating", "N/A")  # Handle cases where rating might not be available
                        # cast = movie_info.get("cast", [])
                        # You can limit the cast to display only the top few actors if needed
                        plot = movie_info.get('plot outline', 'Plot summary not available')
                        ui.terminalPrint(
                            f"{title} was released in {year} and has an IMDb rating of {rating}.\n"
                            f"The plot summary of the movie is: {plot}\n"
                        )
                        speak(f"{title} was released in {year} and has an IMDb rating of {rating}."
                              f"The plot summary of the movie is: {plot}\n")
                        break
                elif ('exit program' in query) or ('jarvis sleep' in query):
                    if query == "jarvis sleep":
                        ui.updateMovieDynamically("sleeping")
                        ui.terminalPrint(" Ok sir I'm sleeping, BYE!")
                        speak(" Ok sir I'm sleeping, BYE!")
                    else:
                        ui.updateMovieDynamically("sleeping")
                        ui.terminalPrint("I'm leaving Sir, BYE!")
                        speak("I'm leaving Sir , BYE!")
                    running = False  # Set the flag too False to exit the loop
                elif "close" in query:
                    ui.terminalPrint(f"I am closing sir")
                    speak(f"I am {query} sir")
                    time.sleep(2)  # Adjust the time as needed.
                    pyautogui.hotkey('alt', 'f4')  # Close the active window
                elif ("jarvis search" in query) or ("jarvis " in query) or ("" in query):  # or ("" in query)
                    from gemin_config import send_request
                    speak(f"I am searching sir {query}")
                    try:
                        query = query.replace("jarvis", "")
                        query = send_request(f"{query}")
                        ui.terminalPrint(f"AI Response: {query}\n")
                        speak(query)
                    except:
                        speak("No Results found Sir how can I help you...")
                        ui.terminalPrint("No results Found")


startExecution = jarvisMainClass()


class jarvis_main_windows(QDialog):

    def __init__(self):
        super(jarvis_main_windows, self).__init__()
        print("Setting Up GUI")
        self.jarvisUI = Ui_jarvis_main_gui()
        self.jarvisUI.setupUi(self)

        self.jarvisUI.exit_Button.clicked.connect(self.close)
        self.jarvisUI.enter_Button.clicked.connect(self.manualCodeFromTerminal)
        self.runAllMovies()

    def manualCodeFromTerminal(self):
        if self.jarvisUI.Text_enter.text():
            cmd = self.jarvisUI.Text_enter.text()
            self.jarvisUI.Text_enter.clear()
            self.jarvisUI.terminalinputBox.appendPlainText(f"You typed-> {cmd}")

            if cmd == 'exit':
                ui.close()
            elif cmd == 'help':
                self.terminalPrint(speak("I can perform various tasks which is programmed by Gopi sir."

                                         "Examples are: Time, Wikipedia, Play music, "
                                         "close windows, open any system applications,"
                                         "Google search,wikipedia search, Play YouTube video,  "
                                         " google ai  gemini support"))

            elif cmd == 'start':
                startExecution.start()

            else:
                pass

    def terminalPrint(self, text):
        self.jarvisUI.terminalinputBox.appendPlainText(text)

    def updateMovieDynamically(self, state):
        if state == "speaking":
            self.jarvisUI.speaking_label.raise_()
            self.jarvisUI.speaking_label.show()
            self.jarvisUI.listening_label.hide()
            self.jarvisUI.loading_label.hide()
            self.jarvisUI.sleeping_label.hide()

        elif state == "listening":
            self.jarvisUI.listening_label.raise_()
            self.jarvisUI.listening_label.show()
            self.jarvisUI.speaking_label.hide()
            self.jarvisUI.loading_label.hide()
            self.jarvisUI.sleeping_label.hide()

        elif state == "loading":
            self.jarvisUI.loading_label.raise_()
            self.jarvisUI.loading_label.show()
            self.jarvisUI.speaking_label.hide()
            self.jarvisUI.listening_label.hide()
            self.jarvisUI.sleeping_label.hide()
        elif state == "sleeping":
            self.jarvisUI.sleeping_label.raise_()
            self.jarvisUI.sleeping_label.show()
            self.jarvisUI.loading_label.hide()
            self.jarvisUI.speaking_label.hide()
            self.jarvisUI.listening_label.hide()

    def runAllMovies(self):

        self.jarvisUI.codingMovie = QtGui.QMovie("images\\tony-stark.gif")
        self.jarvisUI.coding_animation.setMovie(self.jarvisUI.codingMovie)
        self.jarvisUI.codingMovie.start()

        self.jarvisUI.listeningMovie = QtGui.QMovie("images\\listening.gif")
        self.jarvisUI.listening_label.setMovie(self.jarvisUI.listeningMovie)
        self.jarvisUI.listeningMovie.start()

        self.jarvisUI.speakingMovie = QtGui.QMovie("images\\VAQa.gif")
        self.jarvisUI.speaking_label.setMovie(self.jarvisUI.speakingMovie)
        self.jarvisUI.speakingMovie.start()

        self.jarvisUI.arcMovie = QtGui.QMovie("images\\sleeping_img.gif")
        self.jarvisUI.Ar_Reactor.setMovie(self.jarvisUI.arcMovie)
        self.jarvisUI.arcMovie.start()

        self.jarvisUI.arcMovie1 = QtGui.QMovie("images\\side_img.gif")
        self.jarvisUI.Ar_Reactor_2.setMovie(self.jarvisUI.arcMovie1)
        self.jarvisUI.arcMovie1.start()

        self.jarvisUI.Iron_Man = QtGui.QMovie("images\\center_img.gif")
        self.jarvisUI.Iron_Man_IMG.setMovie(self.jarvisUI.Iron_Man)
        self.jarvisUI.Iron_Man.start()

        self.jarvisUI.loadingMovie = QtGui.QMovie("images\\loading.gif")
        self.jarvisUI.loading_label.setMovie(self.jarvisUI.loadingMovie)
        self.jarvisUI.loadingMovie.start()

        self.jarvisUI.sleepingMovie = QtGui.QMovie("images\\sleep.gif")
        self.jarvisUI.sleeping_label.setMovie(self.jarvisUI.sleepingMovie)
        self.jarvisUI.sleepingMovie.start()

        startExecution.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = jarvis_main_windows()
    ui.show()
    sys.exit(app.exec_())
