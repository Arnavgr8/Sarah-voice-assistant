import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine once
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[1].id)
engine.setProperty("rate", 200)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        # Add energy threshold adjustment
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.5  # Increased pause threshold to give more time
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout and phrase time limit
            print("Processing...")
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        return query
    except sr.UnknownValueError:
        return "none"
    except sr.RequestError:
        print("Could not request results; check your internet connection")
        return "none"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "none"