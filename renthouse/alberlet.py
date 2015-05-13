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

    def get_urls(self):
         _lastPage = int(self.__get_max_page_number())
         #print("lastpage: "+str(_lastPage))
         for pageNumber in range(1, _lastPage + 1):
             #print ("pageNumber: " + str(pageNumber))
             self.__get_page_urls(pageNumber)
         return self.numberOflinks

    def __get_page_urls(self, pageNum):
        response = requests.get(self.url+"/page:"+str(pageNum))
        soup = bs4.BeautifulSoup(response.text)
        # find the rent box div
        divs = soup.find_all('div', attrs={'class': 'listing-item'})
        # print(divs)
        for div in divs:
            self.numberOflinks += 1
            link = self.__get_link(div)
            street = self.__get_address(div)
            price = self.__get_price(div)
            size = self.__get_area_size(div)
            self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}

    def __get_area_size(self, div):
        _p = div.find('p', attrs={'class': 'listing-rooms'})
        _size = _p.find('b').text
        _size = ''.join(_size.split())
        # remove m2 string from the end
        _size = _size[:-2]
        return _size

    def __get_max_page_number(self):
        _response = requests.get(self.url + "/page:last")
        _soup = bs4.BeautifulSoup(_response.text)
        _max = _soup.find('li', attrs={'class': 'current'})
        if (_max == None):
            return 1
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
