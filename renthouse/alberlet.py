__author__ = 'speky'
import requests
import bs4
import operator

root_url = 'http://alberlet.hu'
index_url = root_url + '/kiado_alberlet/ingatlan-tipus:lakas/keres:advanced/limit:48/megye:budapest/'
# '/kiado_alberlet/berleti-dij:0-50-ezer-ft/ingatlan-tipus:lakas/ingatlan:tegla/limit:48'
berendezes_string = "/berendezes:2"
kisallat_string = "/haziallat-engedelyezve:igen"
tegla_string = "/ingatlan:tegla"
kerulet_string = "/kerulet:"
meret_string = "/meret:"
dij_string = "berleti-dij:"


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
    # print(divs)

    rentHouses = {}  # dictionary

    for div in divs:
        # link = get_link(div)
        # street = get_address(div)
        # price = get_price(div)
        # size = get_area_size(div)
        rentHouses ={
            'abc': {'address': 'street1', 'price': '15', 'size': '1', 'distance': '20'},
            'dfg': {'address': 'street2', 'price': '15', 'size': '3', 'distance': '200'},
            'wer': {'address': 'street2', 'price': '13', 'size': '2', 'distance': '100'}
        }

        items = rentHouses.items()

        sorted_items = sorted(items, key=lambda kvt: (kvt[1]['price'], kvt[1]['distance']))

        for key, values in sorted_items:
            print(values)


            # LAST_PAGE = int(get_max_page_number())
            # print LAST_PAGE
            # linkLists = []

            #for pageNumber in range(1, LAST_PAGE + 1):
            #    print "pageNumber: " + str(pageNumber)
            #   linkLists.append(get_video_page_urls(index_url + '/page:' + str(pageNumber)))

            #for list in linkLists:
            #    for elem in list:
            #        print(elem)