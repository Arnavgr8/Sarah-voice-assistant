import wikipedia
from core.speech import speak
from core.web import get_location
import requests
from bs4 import BeautifulSoup

def get_wikipedia_info(query):
    try:
        speak("searching wikipedia....")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("according to wikipedia")
        speak(results)
    except:
        speak("something went wrong....")

def get_weather():
    city, country = get_location()
    if city and country:
        search = f"temperature in {city} {country}"
        url = f"https://google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"current {search} is {temp}celsius")
    else:
        speak("Sorry, I couldn't get the weather information")

def get_person_info():
    from core.speech import speak, takecommand
    
    speak("Which person's information would you like to know?")
    person = takecommand().lower()
    if person != "none":
        try:
            info = wikipedia.summary(person, sentences=2)
            speak(info)
        except Exception as e:
            speak(f"Could not find information about {person}")

def tell_date():
    import datetime
    from core.speech import speak
    
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {current_date}")

def tell_time():
    import datetime
    from core.speech import speak
    
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")