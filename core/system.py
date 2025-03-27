from core.app_scanner import get_installed_apps
from core.speech import speak
import os
import datetime as dt
import time
import psutil

# Add at the top
import json
from pathlib import Path
import ollama

# Replace hardcoded paths with configurable ones
CONFIG_PATH = Path(__file__).parent.parent / 'config'

def load_config():
    """Load path configuration"""
    with open(CONFIG_PATH / 'paths.json') as f:
        return json.load(f)

def resolve_path(path_pattern):
    """Resolve path patterns with environment variables"""
    return os.path.expandvars(path_pattern)

def find_matching_app(app_name):
    """Fuzzy match app name against installed applications"""
    installed_apps = get_installed_apps()
    app_name = app_name.lower()
    
    # Check for direct matches first
    for app in installed_apps:
        if app_name in app['name'].lower() or app_name == app['name'].lower():
            return app
    
    # Check partial matches
    for app in installed_apps:
        if app_name in app['name'].lower() or app['name'].lower().startswith(app_name):
            return app
    
    return None

def launch_app(app_name):
    """Launch application using scanned app data"""
    try:
        matched_app = find_matching_app(app_name)
        
        if matched_app:
            # Handle directory paths by looking for common executables
            if os.path.isdir(matched_app['path']):
                exe_path = find_exe_in_directory(matched_app['path'])
                if exe_path:
                    os.startfile(exe_path)
                    return
                else:
                    raise FileNotFoundError
            else:
                os.startfile(matched_app['path'])
                return
                
        # Fallback to hardcoded paths if no match
        if app_name == 'task_manager':
            os.startfile("C:\\Windows\\System32\\Taskmgr.exe")
        elif app_name == 'explorer':
            os.startfile("C:\\Windows\\explorer.exe")
        elif app_name == 'system_info':
            os.startfile("C:\\Windows\\System32\\msinfo32.exe")
        elif app_name == 'control_panel':
            os.startfile("C:\\Windows\\System32\\control.exe")
        elif app_name == 'cmd':
            os.startfile("C:\\Windows\\System32\\cmd.exe")
        elif app_name == 'powershell':
            os.startfile("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe")

        # Basic Windows apps
        elif app_name == 'calculator':
            os.startfile("C:\\Windows\\System32\\calc.exe")
        elif app_name == 'notepad':
            os.startfile("C:\\Windows\\System32\\notepad.exe")
        elif app_name == 'paint':
            os.startfile("C:\\Windows\\System32\\mspaint.exe")
        
        # Microsoft Office
        elif app_name == 'word':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
        elif app_name == 'excel':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
        elif app_name == 'powerpoint':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
        elif app_name == 'outlook':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE")
        elif app_name == 'onenote':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE")

        # Browsers
        elif app_name == 'chrome':
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        elif app_name == 'firefox':
            os.startfile("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
        elif app_name == 'edge':
            os.startfile("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
        elif app_name == 'opera':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Opera\\launcher.exe")
        
        # Development tools
        elif app_name == 'vscode':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        elif app_name == 'pycharm':
            os.startfile("C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.1\\bin\\pycharm64.exe")
        elif app_name == 'git':
            os.startfile("C:\\Program Files\\Git\\git-bash.exe")
        elif app_name == 'postman':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Local\\Postman\\Postman.exe")

        # Media and Entertainment
        elif app_name == 'vlc':
            os.startfile("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe")
        elif app_name == 'spotify':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe")
        elif app_name == 'itunes':
            os.startfile("C:\\Program Files\\iTunes\\iTunes.exe")
        elif app_name == 'winamp':
            os.startfile("C:\\Program Files (x86)\\Winamp\\winamp.exe")

        # Communication
        elif app_name == 'discord':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe")
        elif app_name == 'teams':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe")
        elif app_name == 'skype':
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\lync.exe")
        elif app_name == 'zoom':
            os.startfile("C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")

        # Gaming and Entertainment
        elif app_name == 'steam':
            os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
        elif app_name == 'epic':
            os.startfile("C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe")
        elif app_name == 'battle_net':
            os.startfile("C:\\Program Files (x86)\\Battle.net\\Battle.net Launcher.exe")
        elif app_name == 'origin':
            os.startfile("C:\\Program Files (x86)\\Origin\\Origin.exe")

        else:
            speak(f"Sorry, I couldn't find the application {app_name}")
    except Exception as e:
        speak(f"Error starting {app_name}: {str(e)}")

def check_internet_speed():
    """Measure internet speed using speedtest-cli"""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        return {
            'download': f"{st.download()/1_000_000:.2f} Mbps",
            'upload': f"{st.upload()/1_000_000:.2f} Mbps"
        }
    except Exception as e:
        return f"Speed test failed: {str(e)}"

def handle_system_commands(query):
    pass


def handle_unknown_command(query):
    """Handle unknown commands using a multilingual LLM"""
    # Only process if query has more than one word
    if len(query.split()) > 1:
        try:
            # Import ollama only when needed to avoid startup overhead
            
            response = ollama.chat(
                model='tinyllama',  # Multilingual model
                messages=[{
                    'role': 'system',
                    'content': "Your name is Sarah. Give short replies only"
                },
                {
                    'role': 'user',
                    'content': query.strip()  # Clean input
                }],
                options={
                    'temperature': 0.5,
                    'top_p': 0.9,
                    'max_tokens': 50
                }
            )
            
            if response and 'message' in response and 'content' in response['message']:
                speak(response['message']['content'].strip())
            else:
                speak("I received an invalid response")
                
        except ImportError:
            speak("Sorry, the language model is not available")
        except Exception as e:
            print(f"Sorry, I encountered an error: {str(e)}")
    


# System information dictionary initialization
SYSTEM_INFO = {
    'paths': {},
    'apps': [],
    'config_loaded': False,
    'battery': None
}

def update_battery_info():
    """Update battery information in SYSTEM_INFO"""
    try:
        SYSTEM_INFO['battery'] = psutil.sensors_battery()
    except Exception:
        SYSTEM_INFO['battery'] = None

# Update battery info before checking
def wish():
    update_battery_info()
    hour = int(dt.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak("good morning sir!")
    elif hour >= 12 and hour <= 17:
        speak("good afternoon sir!")
    elif hour >= 17 and hour <= 23:
        speak("good evening sir!")
    elif hour >= 23 and hour <= 4:
        speak("Sir you may sleep now")

    # Check battery only if available
    if SYSTEM_INFO['battery'] and SYSTEM_INFO['battery'].percent <= 20:
        speak(f"Sir, battery is low. Only {SYSTEM_INFO['battery'].percent}% remaining")

    speak(f"its {tt}")
    if SYSTEM_INFO['battery'].percent <= 20:
        speak(f"Low battery warning: {SYSTEM_INFO['battery'].percent}% remaining")
    else:
        speak("We are okay with battery")
    speak("I am Sarah please tell me how can I help you")
