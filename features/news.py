import requests
from bs4 import BeautifulSoup
from core.speech import speak

def get_tech_news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=56d287c3f2784a709d4e2e5ead3d7676'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    for article in articles:
        speak(article["title"])

def get_cricket_news():
    r = requests.get("https://sports.ndtv.com/cricket/news")
    soup = BeautifulSoup(r.content, "html.parser")
    headlines = soup.find_all("p", class_="lst-pg_txt txt_tct txt_tct-three")
    for headline in headlines:
        speak(headline.text)

def get_football_news():
    r = requests.get("https://www.bbc.com/sport/football")
    soup = BeautifulSoup(r.content, "html.parser")
    headline1 = soup.find("h3", class_="gs-c-promo-heading__title gel-double-pica-bold sp-o-link-split__text")
    headlines = soup.find_all("h3", class_="gs-c-promo-heading__title gel-pica-bold sp-o-link-split__text")
    speak(headline1.text)
    for headline in headlines:
        speak(headline.text)

def get_pl_standings():
    try:
        p = requests.get("https://www.sportskeeda.com/go/epl/standings")
        soup = BeautifulSoup(p.content, "html.parser")
        
        all_teams = soup.find_all(class_="keeda_football_table_team_name")
        all_teams_points = soup.find_all("td", class_="overall-points")
        all_teams_position = soup.find_all(class_="value")
        
        for team, position, points in zip(all_teams, all_teams_position, all_teams_points):
            speak(f"{team.text.strip()} is at position {position.text.strip()} with {points.text.strip()} points")
    except Exception as e:
        speak(f"Could not retrieve Premier League standings: {str(e)}")

def get_laliga_standings():
    try:
        r = requests.get("https://www.theguardian.com/football/laligafootball/table")
        soup = BeautifulSoup(r.content, "html.parser")
        
        all_team_names = soup.find_all("a", class_="team-name__long")
        all_team_positions = soup.find_all("td", class_="table-column--sub")
        all_team_points = soup.find_all("b")
        
        for name, position, points in zip(all_team_names, all_team_positions, all_team_points):
            cleaned_name = name.text.strip().replace("\n", "")
            speak(f"{cleaned_name} is at position {position.text.strip()} with {points.text.strip()} points")
    except Exception as e:
        speak(f"Could not retrieve La Liga standings: {str(e)}")