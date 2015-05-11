__author__ = 'speky'
import requests
import bs4
import operator
import base


class AlberletSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
        self.root_url = 'http://alberlet.hu'
        self.index_url = self.root_url + '/kiado_alberlet/ingatlan-tipus:lakas/keres:advanced/limit:48/megye:budapest'
        # '/kiado_alberlet/berleti-dij:0-50-ezer-ft/ingatlan-tipus:lakas/ingatlan:tegla/limit:48'
        self.tegla_string = "/ingatlan:tegla"
        self.furniture_string = "/berendezes:2"
        self.dog_string = "/haziallat-engedelyezve:igen"
        self.district_string = "/kerulet:"
        self.size_string = "/meret:"
        self.cost_string = "/berleti-dij:"

    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url + self.tegla_string
        if len(str(district)) > 0:
            self.url += self.district_string
            self.url += str(district)

        if dog == 1:
            self.url += self.dog_string

        if furniture == 1:
            self.url += self.furniture_string

        self.url += self.size_string+str(min_size)+"-"+str(max_size)+"-m2"
        self.url += self.cost_string+str(min_cost)+"-"+str(max_cost)+"-ezer-ft"

        print(self.url)

    def get_page_urls(self):
        response = requests.get(self.url)
        soup = bs4.BeautifulSoup(response.text)

        # find the rent box div
        divs = soup.find_all('div', attrs={'class': 'listing-item'})
        # print(divs)

        self.rentHouses = {}  # dictionary
        for div in divs:
            self.numberOflinks += 1
            link = self.__get_link(div)
            street = self.__get_address(div)
            price = self.__get_price(div)
            size = self.__get_area_size(div)
            self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}

            #self.rentHouses ={
            #    'abc': {'address': 'street1', 'price': '15', 'size': '1', 'distance': '20'},
            #    'dfg': {'address': 'street2', 'price': '15', 'size': '3', 'distance': '200'},
            #    'wer': {'address': 'street2', 'price': '13', 'size': '2', 'distance': '100'}
            #}

            #items = self.rentHouses.items()
            #sorted_items = sorted(items, key=lambda kvt: (kvt[1]['price'], kvt[1]['distance']))
            #for key, values in sorted_items:
            #    print(values)

            # LAST_PAGE = int(get_max_page_number())
            #for pageNumber in range(1, LAST_PAGE + 1):
            #    print "pageNumber: " + str(pageNumber)
            #   linkLists.append(get_video_page_urls(index_url + '/page:' + str(pageNumber)))

            #for list in linkLists:
            #    for elem in list:
            #        print(elem)
        items = self.rentHouses.items()
        sorted_items = sorted(items, key=lambda kvt: (kvt[1]['price'], kvt[1]['distance']))
        for key, values in sorted_items:
            print(values)

        return self.numberOflinks

    def __get_area_size(self, div):
        _p = div.find('p', attrs={'class': 'listing-rooms'})
        _size = _p.find('b').text
        _size = ''.join(_size.split())
        # remove m2 string from the end
        _size = _size[:-2]
        return _size

    def __get_max_page_number(self):
        _response = requests.get(self.index_url + "/page:last")
        _soup = bs4.BeautifulSoup(_response.text)
        _max = _soup.find('li', attrs={'class': 'current'})
        return _max.text

    def __get_link(self, div):
        address = div.find('div', attrs={'class': 'box-grid-head'})
        _link = address.find('a')['href']
        if _link.startswith('/'):
            return self.root_url + _link
        return _link

    def __get_address(self, div):
        _district = div.find('h4', attrs={'class': 'city-with-info'}).text
        _address = div.find('div', attrs={'class': 'box-grid-head'})
        _street = _address.find('a').text
        return _district.strip() + ' ' + _street

    def __get_price(self, div):
        _p = div.find('p', attrs={'class': 'listing-rent'})
        _price = _p.find('b').text
        _price = ''.join(_price.split())
        # remove HUF string from the end
        _price = _price[:-3]
        return _price
