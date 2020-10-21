from bs4 import BeautifulSoup
import requests

data = {
    "wins": "PVPMatchsWon"
}
url_tracker = "https://r6.tracker.network/profile/pc/"

def get_general(nick):
    url = url_tracker + nick
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.find('div', {'data-stat': 'PVPMatchesWon'})
    return int(convert.contents[0])

print(get_general("KriptYashka"))