import pyjokes
import pywhatkit as kit
from core.speech import speak, takecommand
import features.lyrics as lyrics

def tell_joke():
    speak(pyjokes.get_joke())

def play_youtube_video():
    speak("which video do u want me to play?")
    video = takecommand().lower()
    if video != "none":
        kit.playonyt(video)
    else:
        speak("no such video found")

def play_music(music_dir):
    import os
    songs = os.listdir(music_dir)
    for song in songs:
        if song.endswith('.mp3'):
            os.startfile(os.path.join(music_dir, song))

def search_lyrics(song):
    if song != "none":
        try:
            result = lyrics.get_song_lyrics(song)
            if result:
                speak(f"Here are the lyrics for {song}")
                print(result)
                return True
            else:
                speak(f"Sorry, I couldn't find the lyrics for {song}")
                return False
        except lyrics.LyricsError as e:
            speak(str(e))
            return False
    else:
        speak("I didn't catch the song name. Please try again.")
        return False
        

def get_word_meaning():
    import webbrowser
    from core.speech import speak, takecommand
    
    speak("Which word's meaning would you like to search?")
    word = takecommand().lower()
    if word != "none":
        import threading
        threading.Thread(target=lambda: webbrowser.open(f"https://www.google.com/search?q=define+{word}")).start()
    else:
        speak("Could not recognize the word")