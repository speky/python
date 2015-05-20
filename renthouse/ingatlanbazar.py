__author__ = 'speky'

import requests
import bs4
import operator
import base


class IngatlanBazarSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
        self.root_url = 'http://ingatlanbazar.hu/'
        self.index_url = self.root_url + '/HU/ingatlan-'
        self.districts = {'I':202, 'II':197, 'III': 213, 'IV':199, 'V':208, 'VI':212, 'VII':217, 'VIII':214, 'IX':216, 'X':204,
                          'XI':209, 'XII':205, 'XIII':210, 'XIV':211, 'XV':206,'XVI':201, 'XVII':196, 'XVIII':245, 'XIX':198, 'XX':200,
                          'XXI':207, 'XXII':203, 'XXIII':218}

    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url
        self.url += '+'+self.__set_district(district)
        if furniture == 1:
            self.url += self.furniture_string
        # self.url += "+"+str(min_size)+"-"+str(max_size)+"-m2"
        self.url += self.cost_string+str(min_cost)+"-"+str(max_cost)+"-ezer-Ft"
        print(self.url)

    def get_urls(self):
        _lastPage = int(self.__get_max_page_number())
        print("lastpage: "+str(_lastPage))
        for pageNumber in range(1, _lastPage + 1):
            # print ("pageNumber: " + str(pageNumber))
            self.__get_page_urls(pageNumber)
        return self.numberOflinks

    def __get_max_page_number(self):
            _response = requests.get(self.url)
            # fix if bug in the response html
            text = _response.text.replace("!–[", "!--[")
            _soup = bs4.BeautifulSoup(text)
            _max = _soup.find('li', attrs={'class': 'numbers'})
            if _max == None:
                return 0
            _maxTxt = _max.text
            _maxTxt = _maxTxt.replace('\n', '')
            # get max page number
            _pageNum = _maxTxt.split()[-1]
            #truncate '-bol' string from the end of it
            return _pageNum[:-4]

    def __get_page_urls(self, pageNum):
        _response = requests.get(self.url+"?page="+str(pageNum))
        # fix if bug in the response html
        _text = _response.text.replace("!–[", "!--[")
        _soup = bs4.BeautifulSoup(_text)
        # find the rent box div
        _divs = _soup.find_all('tr', attrs={'class': 'list-row'})
        for div in _divs:
            self.numberOflinks += 1
            link = self.__get_link(div)
            street = self.__get_address(div)
            price = self.__get_price(div)
            size = self.__get_area_size(div)
            self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}

    def __set_district(self, district):
        if len(district) == 0:
            return "Magyarorszag-Lakas-Kiado-8-10-2"
        _result = "Magyarorszag-Lakas-Kiado-8-10-"
        for num in district.split('+'):
            id = num
            id = str(id).upper()
            _result += str(self.districts[id]) + ','
        _result = _result[:-1]
        print(_result)
        return _result

    def __get_link(self, div):
        address = div.find('td', attrs={'class': 'thumbnail'})
        _link = address.find('a')['href']
        if _link.startswith('/'):
            return self.root_url + _link
        return _link

    def __get_address(self, div):
        _section = div.find('td', attrs={'class': 'address'})
        _district = _section.text
        _address = _district.replace('\n', '').strip()
        return _address

    def __get_area_size(self, div):
        _results = div.find_all('td', attrs={'class': 'centered'})
        _size = _results[1].text
        _size = ''.join(_size.split())
        # remove m2 string from the end
        return _size[:-2]

    def __get_price(self, div):
        _price = div.find('td', attrs={'class': 'centered'})
        _price = _price.text
        _price = ''.join(_price.split())
        return _price[:-5]
