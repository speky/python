__author__ = 'speky'
import requests
import bs4

root_url = 'http://alberlet.hu'
index_url = root_url + '/kiado_alberlet/berleti-dij:0-50-ezer-ft/ingatlan-tipus:lakas/ingatlan:tegla/limit:48'

def get_max_page_number():
    response = requests.get(index_url+"/page:last")
    soup = bs4.BeautifulSoup(response.text)
    max = soup.find('li', attrs={'class' : 'current'})
    return max.text

def get_video_page_urls(uri):
    response = requests.get(uri)
    soup = bs4.BeautifulSoup(response.text)

    links = []
    divs = soup.find_all('div', attrs={'class' : 'listing-image'})

    for div in divs:
        link = div.find('a')['href']
        #print link
        if link.startswith('/'):
            links.append(root_url + link)
            #print link
            #print root_url+link
        else:
           links.append(link)
    return links

#LAST_PAGE = int(get_max_page_number())
#print LAST_PAGE
linkLists = []
#for pageNumber in range(1, LAST_PAGE + 1):
#    print "pageNumber: " + str(pageNumber)
 #   linkLists.append(get_video_page_urls(index_url + '/page:' + str(pageNumber)))

for list in linkLists:
    for elem in list:
       print (elem)