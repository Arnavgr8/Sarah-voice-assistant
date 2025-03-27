import winreg
import json
import os
import glob
from pathlib import Path
import win32com.client  # Requires pywin32

apps = []

def get_start_menu_apps():
    """Scan Start Menu shortcuts for applications"""
    
    shell = win32com.client.Dispatch("WScript.Shell")
    
    # Scan both user and all-users start menu
    start_menu_paths = [
        os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    ]
    
    for start_path in start_menu_paths:
        for filepath in glob.glob(os.path.join(start_path, '**', '*.lnk'), recursive=True):
            try:
                shortcut = shell.CreateShortCut(filepath)
                target_path = shortcut.Targetpath
                
                if os.path.exists(target_path):
                    apps.append({
                        'name': Path(filepath).stem,
                        'path': os.path.normpath(target_path)
                    })
            except Exception as e:
                continue
                
    return apps

def get_installed_apps():
    """Combine registry and Start Menu apps"""
    registry_apps = []
    registry_locations = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for hive, subkey in registry_locations:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    app_key_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, app_key_name) as app_key:
                        try:
                            name = winreg.QueryValueEx(app_key, "DisplayName")[0]
                            install_path = winreg.QueryValueEx(app_key, "InstallLocation")[0]
                            
                            # Validate path exists
                            if install_path and Path(install_path).exists():
                                apps.append({
                                    'name': name.strip(),
                                    'path': os.path.normpath(install_path)
                                })
                        except FileNotFoundError:
                            continue
        except FileNotFoundError:
            continue

    # Combine both sources and remove duplicates
    combined = {app['path']: app for app in registry_apps + get_start_menu_apps()}
    return list(combined.values())

def save_apps_to_json(apps, filename="installed_apps.json"):
    """Save list of apps to JSON file"""
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=2)

if __name__ == "__main__":
    installed_apps = get_installed_apps()
    print(f"Found {len(installed_apps)} installed applications")
    save_apps_to_json(installed_apps)
    print("Results saved to installed_apps.json")