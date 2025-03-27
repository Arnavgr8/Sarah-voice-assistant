import webbrowser
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from core.speech import speak

def open_website(url):
    webbrowser.open(url)

def search_google(query):
    for url in search(query, stop=1):
        webbrowser.open(url)

def get_location():
    try:
        ipAdd = requests.get("https://api.ipify.org").text
        url = "https://get.geojs.io/v1/ip/geo/" + ipAdd + ".json"
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        return geo_data["city"], geo_data["country"]
    except Exception:
        return None, None

def get_ip_address():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Unable to retrieve IP address"

def get_current_location():
    try:
        ip = get_ip_address()
        url = f"https://get.geojs.io/v1/ip/geo/{ip}.json"
        response = requests.get(url)
        data = response.json()
        return {
            "city": data.get("city"),
            "country": data.get("country"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    except Exception as e:
        speak(f"Location error: {str(e)}")
        return None