__author__ = 'speky'

import requests
import bs4
import operator
import base

class IngatlanSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
        self.root_url = 'http://ingatlan.com'
        self.index_url = self.root_url + '/szukites/kiado+lakas+tegla-epitesu-lakas'
        self.furniture_string = "+butorozott"
        self.dog_string = "+kisallat-hozhato"
        self.cost_string = "+havi-"

    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url
        if len(str(district)) > 0:
            self.url += '+'+self.__set_district(district)
        if dog == 1:
            self.url += self.dog_string
        if furniture == 1:
            self.url += self.furniture_string
        #self.url += "+"+str(min_size)+"-"+str(max_size)+"-m2"
        self.url += self.cost_string+str(min_cost)+"-"+str(max_cost)+"-ezer-Ft"
        print(self.url)


    def get_urls(self):
         _lastPage = int(self.__get_max_page_number())
         print("lastpage: "+str(_lastPage))
         for pageNumber in range(1, _lastPage + 1):
            #print ("pageNumber: " + str(pageNumber))
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
        #print(len(_divs))
        for div in _divs:
            self.numberOflinks += 1
            link = self.__get_link(div)
            street = self.__get_address(div)
            price = self.__get_price(div)
            print(price)
            size = self.__get_area_size(div)
            print(size)
            #self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}

    def __set_district(self, district):
        _result = ""
        _postfix = "-ker"
        for num in district.split('+'):
            _result += num + _postfix + '+'
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
        _size = div.find('div', attrs={'class': 'col-xs-1'}).text
        _size = ''.join(_size.split())
        # remove m2 string from the end
        _size = _size[:-2]
        return _size

    def __get_price(self, div):
        _price = div.find('div', attrs={'class': 'ads_list_price'})
        _price = _price.text
        _price = ''.join(_price.split())
        # remove 'ezer' string from the end
        _price = _price.replace('ezer', '')
        if _price.find('.') == -1:
            _price += "000"
        else:
            _price = _price.replace('.', '')
            _price += "00"
        return _price
