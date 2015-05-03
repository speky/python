__author__ = 'speky'
import requests
import bs4

root_url = 'http://pyvideo.org'
index_url = 'http://alberlet.hu/kiado_alberlet'

#links = soup.select('div.video-summary-data a[href^=/video]')

def get_video_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    return [a.attrs.get('href') for a in soup.select('div.listing-image a[href^=/]')]

print(get_video_page_urls())