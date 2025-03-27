from core.speech import speak, takecommand
from core.system import (
    check_internet_speed,
    wish,
    handle_system_commands,
    handle_unknown_command,
)
from core.web import (
    open_website, search_google, get_ip_address, 
    get_current_location
)
from features.entertainment import (
    tell_joke, play_youtube_video, play_music, 
    search_lyrics, get_word_meaning
)
from features.information import (
    get_wikipedia_info, get_weather, get_person_info,
    tell_date, tell_time
)
from features.news import (
    get_tech_news, get_cricket_news, get_football_news,
    get_pl_standings, get_laliga_standings
)
from features.social import (
    handle_instagram_profile, send_whatsapp_message
)
from features.document import pdf_reader
import settings
import sys
import os
import psutil

# Initialize system information dictionary
SYSTEM_INFO = {}

# Initialize system paths
SYSTEM_INFO['paths'] = settings.get_system_paths()

def handle_command(query):
    # Web commands
    if "open youtube" in query:
        open_website("www.youtube.com")
    elif "open google" in query:
        open_website("https://www.google.com/")
    elif "open facebook" in query:
        open_website("https://www.facebook.com/")
    elif "open twitter" in query:
        open_website("https://twitter.com/")
    elif "open instagram" in query:
        open_website("https://www.instagram.com/")
    elif "open amazon" in query:
        open_website("https://www.amazon.com/")
    elif "open netflix" in query:
        open_website("https://www.netflix.com/")
    elif "open wikipedia" in query:
        open_website("https://www.wikipedia.org/")
    elif "open yahoo" in query:
        open_website("https://www.yahoo.com/")
    elif "open whatsapp" in query:
        open_website("https://web.whatsapp.com/")
    elif "open reddit" in query:
        open_website("https://www.reddit.com/")
    elif "open linkedin" in query:
        open_website("https://www.linkedin.com/")
    elif "open tiktok" in query:
        open_website("https://www.tiktok.com/")
    elif "open pinterest" in query:
        open_website("https://www.pinterest.com/")
    elif "open microsoft" in query:
        open_website("https://www.microsoft.com/")
    elif "open ebay" in query:
        open_website("https://www.ebay.com/")
    elif "open spotify" in query:
        open_website("https://open.spotify.com/")
    elif "open twitch" in query:
        open_website("https://www.twitch.tv/")
    elif "open github" in query:
        open_website("https://github.com/")
    elif "open gmail" in query:
        open_website("https://mail.google.com/")
    elif "open google drive" in query:
        open_website("https://drive.google.com/")
    elif "open google maps" in query:
        open_website("https://maps.google.com/")
    elif "open google docs" in query:
        open_website("https://docs.google.com/")
    elif "open google sheets" in query:
        open_website("https://sheets.google.com/")
    elif "open google slides" in query:
        open_website("https://slides.google.com/")
    elif "open google calendar" in query:
        open_website("https://calendar.google.com/")
    elif "open discord" in query:
        open_website("https://discord.com/")
    elif "open snapchat" in query:
        open_website("https://web.snapchat.com/")
    elif "open microsoft teams" in query:
        open_website("https://teams.microsoft.com/")
    elif "open zoom" in query:
        open_website("https://zoom.us/")
    elif "open slack" in query:
        open_website("https://slack.com/")
    elif "open medium" in query:
        open_website("https://medium.com/")
    elif "open quora" in query:
        open_website("https://www.quora.com/")
    elif "open netflix" in query:
        open_website("https://www.netflix.com/")
    elif "open apple" in query:
        open_website("https://www.apple.com/")
    elif "open bing" in query:
        open_website("https://www.bing.com/")
    elif "open cnn" in query:
        open_website("https://www.cnn.com/")
    elif "open bbc" in query:
        open_website("https://www.bbc.com/")
    elif "open adobe" in query:
        open_website("https://www.adobe.com/")
    elif "open dropbox" in query:
        open_website("https://www.dropbox.com/")
    elif "open paypal" in query:
        open_website("https://www.paypal.com/")
    elif "open walmart" in query:
        open_website("https://www.walmart.com/")
    elif "open target" in query:
        open_website("https://www.target.com/")
    elif "open imdb" in query:
        open_website("https://www.imdb.com/")
    elif "open weather" in query:
        open_website("https://weather.com/")
    elif "open steam" in query:
        open_website("https://store.steampowered.com/")
    elif "open etsy" in query:
        open_website("https://www.etsy.com/")
    elif "open indeed" in query:
        open_website("https://www.indeed.com/")
    elif "open craigslist" in query:
        open_website("https://www.craigslist.org/")
    elif "open stackoverflow" in query:
        open_website("https://stackoverflow.com/")
    elif "open forbes" in query:
        open_website("https://www.forbes.com/")
    elif "open nytimes" in query:
        open_website("https://www.nytimes.com/")
    elif "open espn" in query:
        open_website("https://www.espn.com/")
    elif "video" in query and "youtube" in query:
        play_youtube_video()
    elif "play music" in query:
        music_dir = SYSTEM_INFO['paths'].get('music', os.path.expanduser('~\\Music'))
        play_music(music_dir)
    elif "lyrics" in query:
        while True:
            speak("Which song's lyrics would you like to search?")
            song = takecommand().lower()
            if song != "none":
                search_lyrics(song)
                break
            else:
                speak("I didn't catch that. Could you please repeat the song name?")
    elif "meaning" in query:
        get_word_meaning()

    # Information commands
    elif "temperature" in query or "how's the weather" in query:
        get_weather()
    elif "tell me news" in query:
        get_tech_news()
    elif "cricket news" in query:
        get_cricket_news()
    elif "football news" in query:
        get_football_news()

    # Start application
    elif "start" in query:
        start_application(query)

    # Social commands
    elif "instagram" in query:
        handle_instagram_profile(query)
    
    # PDF reader
    elif "read pdf" in query:
        pdf_reader()

    # System commands
    elif "check battery" in query:
        battery = check_battery()
        speak(f"Battery is at {battery.percent}% and {'charging' if battery.power_plugged else 'not charging'}")
        if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            time_left = dt.timedelta(seconds=battery.secsleft)
            speak(f"Estimated {time_left.hours} hours and {time_left.minutes} minutes remaining")
    
    elif "internet speed" in query:
        speak("Testing internet speed, please wait...")
        speed = check_internet_speed()
        speak(f"Download speed: {speed['download']}, Upload speed: {speed['upload']}")
    
    elif any(x in query for x in ["open task manager", "show task manager", "launch task manager"]):
        start_application('task_manager')
    
    elif any(x in query for x in ["open file explorer", "show files", "open explorer"]):
        start_application('explorer')
    
    elif any(x in query for x in ["open system information", "system info", "computer info"]):
        start_application('system_info')
    
    elif any(x in query for x in ["shut down", "shutdown", "turn off computer"]):
        speak("Shutting down in 5 seconds")
        os.system("shutdown /s /t 5")
    
    elif any(x in query for x in ["restart", "reboot", "restart computer"]):
        speak("Restarting in 5 seconds")
        os.system("shutdown /r /t 5")
    
    elif any(x in query for x in ["sleep", "sleep mode", "sleep the system"]):
        speak("Entering sleep mode")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    elif any(x in query for x in ["hibernate", "hibernation"]):
        speak("Entering hibernation mode")
        os.system("shutdown /h")
    
    elif any(x in query for x in ["switch window", "switch the window", "alt tab"]):
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")
    
    elif "lock computer" in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
    
    elif "sign out" in query:
        os.system("shutdown /l")
    
    elif "system usage" in query:
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        speak(f"CPU usage is {cpu_usage}%")
        speak(f"Memory usage is {memory.percent}%")
        speak(f"Disk usage is {disk.percent}%")

    else:
        handle_unknown_command(query)


def main():
    while True:
        wakeorsleep = takecommand().lower()
        if "wake up" in wakeorsleep or "hello" in wakeorsleep:
            wish()
            while True:
                query = takecommand().lower()
                if "goodbye" in query:
                    speak("Thanks for using me, see you next time, bye")
                    sys.exit()
                elif "sleep" in query:
                    speak("Okay sir, I am going for a nice nap you can call me anytime")
                    break
                else:
                    handle_command(query)
        elif "goodbye" in wakeorsleep:
            speak("Thanks for using me, see you next time, bye")
            sys.exit()

if __name__ == "__main__":
    main()