import os
import re
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize

# Use Google's "I'm Feeling Lucky" to "fuzzy" search for the right page.
SEARCH_URL = "https://www.google.com/search?hl=en&btnI&q=site:www.azlyrics.com"
REDIRECT_RE = r"href=['\"](https?://www.azlyrics.com/[^'\"]*)['\"]"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible)", "Referer": "www.google.com"}

class LyricsError(Exception):
    pass

def sanitize(string):
    """Sanitize string."""
    string = normalize("NFKD", string).encode("ASCII", "ignore")
    string = string.decode("ASCII")
    string = string.lower()
    string = re.sub(r"['\"]+", "", string)
    string = re.sub(r"[([{][^\]})]*[\]})]", "", string)
    string = re.sub(r"^\W+", "", string)
    string = re.sub(r"\W+$", "", string)
    string = re.sub(r"\W+", "+", string, flags=re.ASCII)
    return string

def get_lyrics(song_name):
    """Extract lyrics from azlyrics.com using song name."""
    keyword = sanitize(song_name)
    url = "+".join([SEARCH_URL, keyword, "lyrics"])
    req = requests.get(url, headers=HEADERS)

    # Handle Google's JavaScript redirection
    if re.search(r"unauthorizedredirect", req.text):
        new_url = re.search(REDIRECT_RE, req.text).group(1)
        req = requests.get(new_url, headers=HEADERS)
        req.encoding = "utf-8"

    soup = BeautifulSoup(req.text, features="html.parser")
    div = soup.find("div", attrs={"class": "col-xs-12 col-lg-8 text-center"})
    
    try:
        artist = div.find("div", attrs={"class": "lyricsh"}).find("h2").text
        artist = re.sub(r"(^\s*|\s*Lyrics\s*$)", "", artist)
        title = div.find("b", recursive=False).text
        title = re.sub(r'(^[\s"]*|[\s"]*$)', "", title)
        
        lyrics_divs = div.find_all("div", attrs={"class": None, "id": None})
        if not lyrics_divs:
            raise LyricsError("Could not find lyrics on the page")
            
        lyrics = "\n".join([div.get_text().strip() for div in lyrics_divs])
        return {
            "artist": artist,
            "title": title,
            "lyrics": lyrics,
            "url": req.url
        }
        
    except (AttributeError, LyricsError) as e:
        raise LyricsError(f"Error retrieving lyrics for '{song_name}'. Please check the song name and try again.")

def get_song_lyrics(song_name):
    """Main function to get lyrics for a song."""
    try:
        result = get_lyrics(song_name)
        return f"{result['artist']} - {result['title']}\n\n{result['lyrics']}"
    except LyricsError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
