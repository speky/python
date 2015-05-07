__author__ = 'speky'
import requests
import bs4

root_url = 'http://alberlet.hu'
index_url = root_url + '/kiado_alberlet/ingatlan-tipus:lakas/kerulet:xxiii/megye:budapest/keres:advanced/limit:32'
# '/kiado_alberlet/berleti-dij:0-50-ezer-ft/ingatlan-tipus:lakas/ingatlan:tegla/limit:48'

def get_max_page_number():
    _response = requests.get(index_url + "/page:last")
    _soup = bs4.BeautifulSoup(_response.text)
    _max = _soup.find('li', attrs={'class': 'current'})
    return _max.text


def get_link(div):
    address = div.find('div', attrs={'class': 'box-grid-head'})
    _link = address.find('a')['href']
    if _link.startswith('/'):
        return root_url + _link
    return _link


def get_address(div):
    _district = div.find('h4', attrs={'class': 'city-with-info'}).text
    _address = div.find('div', attrs={'class': 'box-grid-head'})
    _street = _address.find('a').text
    return _district.strip() + ' ' + _street


def get_price(div):
    _p = div.find('p', attrs={'class': 'listing-rent'})
    _price = _p.find('b').text
    _price = ''.join(_price.split())
    # remove HUF string from the end
    _price = _price[:-3]
    return _price


def get_area_size(div):
    _p = div.find('p', attrs={'class': 'listing-rooms'})
    _size = _p.find('b').text
    _size = ''.join(_size.split())
    # remove m2 string from the end
    _size = _size[:-2]
    return _size


def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)

    # find the rent box div
    divs = soup.find_all('div', attrs={'class': 'listing-item'})
    #print(divs)

    rentHouses = {} # dictionary

    for div in divs:
       # link = get_link(div)
       # street = get_address(div)
       # price = get_price(div)
       # size = get_area_size(div)
        rentHouses['abc'] = ['street1', 'price', 'size1', 2]
        rentHouses['dfg'] = ['street2', 'price', 'size2', 2]
        print(rentHouses)
        for key, values in rentHouses.items():
            print(values[2])

        # LAST_PAGE = int(get_max_page_number())
        # print LAST_PAGE
        # linkLists = []

        #for pageNumber in range(1, LAST_PAGE + 1):
        #    print "pageNumber: " + str(pageNumber)
        #   linkLists.append(get_video_page_urls(index_url + '/page:' + str(pageNumber)))

        #for list in linkLists:
        #    for elem in list:
        #        print(elem)