__author__ = 'speky'
import requests
import bs4

root_url = 'http://pyvideo.org'
index_url = 'http://alberlet.hu/kiado_alberlet'

#links = soup.select('div.video-summary-data a[href^=/video]')

def get_max_page_number():
    response = requests.get(index_url+"/page:1000")
    soup = bs4.BeautifulSoup(response.text)
    max_page = soup.find('li', attrs={'class' : 'current'})
    return max_page.text


def get_video_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)

    print get_max_page_number()
    links = []
    #return [a.attrs["href"] for a in soup.select('div.listing-image')]
    #soup.find_all('a', href=True):
    #for links in [a.attrs["href"] for a in soup.select('div.listing-image')]:
    #     if links['href'] == '' or links['href'].startswith('#'):
    #        continue
    #     print "Found the URL:", links['href']
    divs = soup.find_all('div', attrs={'class' : 'listing-image'})

    for div in divs:
        print div.find('a')['href']


get_video_page_urls()