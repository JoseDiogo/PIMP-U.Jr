import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

def search(text):
    query = urllib.parse.quote(text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    
    return 'https://www.youtube.com' + soup.find(attrs={'class':'yt-uix-tile-link'})['href']
