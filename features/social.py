from core.speech import speak
import webbrowser
import pyautogui
import time

def handle_instagram_profile(username):
    try:
        webbrowser.open(f'https://www.instagram.com/{username}/')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')
    except Exception as e:
        speak(f"Failed to open Instagram profile: {str(e)}")

def send_whatsapp_message(phone, message):
    try:
        webbrowser.open(f'https://web.whatsapp.com/send?phone={phone}&text={message}')
        time.sleep(15)  # Allow time for WhatsApp Web to load
        pyautogui.press('enter')
    except Exception as e:
        speak(f"Failed to send WhatsApp message: {str(e)}")