__author__ = 'speky'

import requests
import bs4
import operator
import base

class RobotSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
        self.root_url = 'http://www.ingatlanrobot.hu'
        self.index_url = self.root_url + '/ingatlanok/kiado-lakas'
        self.furniture_string = "--butor=Igen"
        self.dog_string = "--kisallat=Igen"
        self.district_string = "--varos="
        self.size_string = "--terulet="
        self.cost_string = "--ar="

    def __set_district(self, district):
        _result = ""
        _prefix = "Budapest-"
        _postfix = "-kerulet"
        for num in district.split('+'):
            _result += _prefix + num + _postfix + ','
        _result = _result[:-1]
        print(_result)
        return _result


    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url
        if len(str(district)) > 0:
            self.url += self.district_string
            self.url += self.__set_district(district)
        if dog == 1:
            self.url += self.dog_string
        if furniture == 1:
            self.url += self.furniture_string
        self.url += self.size_string+str(min_size)+"-"+str(max_size)
        self.url += self.cost_string+str(min_cost)+"-"+str(max_cost)
        print(self.url)

    def _pre_check(self):
        uri = self.url+'/oldal1.html'
        response = requests.get(uri)
        soup = bs4.BeautifulSoup(response.text)
        _alert = soup.find('h4', attrs={'class': 'alert'})
        if _alert == None:
            return True
        if _alert.text.startswith('Pontos'):
            return False
        return False

    def get_urls(self):
        if (self._pre_check() == False):
            # search has found nothing
            return 0
        pageNum = 0
        while True:
            pageNum += 1
            response = requests.get(self.url+"/oldal"+str(pageNum)+".html")
            soup = bs4.BeautifulSoup(response.text)
            # find the rent box div
            divs = soup.find_all('div', attrs={'class': 'main_normal_ad'})
            # print(divs)
            for div in divs:
                self.numberOflinks += 1
                link = self.__get_link(div)
                street = self.__get_address(div)
                price = self.__get_price(div)
                size = self.__get_area_size(div)
                self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}
            #print(str(self.numberOflinks))
            _next = soup.find('li', attrs={'class': 'last'})
            # no more page
            if _next == None:
                break
        return self.numberOflinks

    def __get_link(self, div):
        address = div.find('div', attrs={'class': 'col-xs-4'})
        _link = address.find('a')['href']
        if _link.startswith('/'):
            return self.root_url + _link
        return _link

    def __get_address(self, div):
        _section = div.find('h2', attrs={'class': 'ad_t_l1'})
        _district = _section.find('br').text
        _b = bytes(_district, 'ISO 8859-1')
        _address = str(_b.decode('utf-8'))
        _address = _address.replace('\n', '').strip()
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
