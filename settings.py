import os
import shutil
import winreg
from typing import Optional

def get_install_path(app_name: str, reg_key: str) -> Optional[str]:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{reg_key}") as key:
            return winreg.QueryValueEx(key, "InstallLocation")[0]
    except Exception:
        return None

def get_browser_path() -> str:
    for browser in ['brave.exe', 'chrome.exe', 'msedge.exe', 'firefox.exe']:
        if path := shutil.which(browser):
            return path
    return os.path.expandvars(r"%PROGRAMFILES%\\BraveSoftware\\Brave-Browser\\Application\\Brave.exe")

def get_spotify_path() -> str:
    if install_path := get_install_path('Spotify', 'Spotify'):
        exe_path = os.path.join(install_path, 'Spotify.exe')
        if os.path.exists(exe_path):
            return exe_path
    return os.path.expandvars(r"%APPDATA%\\Spotify\\Spotify.exe")

def get_editor_path(editor: str) -> str:
    if path := shutil.which(editor):
        return path
    return os.path.join(os.environ.get('SystemRoot', r'C:\\Windows'), 'system32', f'{editor}.exe')

def get_system_paths() -> dict:
    return {
        'notepad': get_editor_path('notepad'),
        'browser': get_browser_path(),
        'spotify': get_spotify_path(),
        'vscode': get_install_path('VSCode', '{771FD6B0-FA20-440A-A002-3B3BAC16DC50}_is1') or r"%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe",
    }