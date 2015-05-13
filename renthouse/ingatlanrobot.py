__author__ = 'speky'
<<<<<<< HEAD
=======

# /kiado-lakas--varos=Budapest-XIV-kerulet,Budapest-XVI-kerulet--ar=0-80--butor=Igen--kisallat=Igen--terulet=30-80/
>>>>>>> robot
import requests
import bs4
import operator
import base

<<<<<<< HEAD
=======

>>>>>>> robot
class RobotSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
<<<<<<< HEAD
        self.root_url = 'http://ingatlanrobot.hu/ingatlanok'
        self.index_url = self.root_url + '/kiado-lakas--ar=0-50'
=======
        self.root_url = 'http://www.ingatlanrobot.hu/ingatlanok'
        self.index_url = self.root_url + '/kiado-lakas'
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
>>>>>>> robot

    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url
        if len(str(district)) > 0:
            self.url += self.district_string
<<<<<<< HEAD
            self.url += str(district)
=======
            self.url += self.__set_district(district)
>>>>>>> robot
        if dog == 1:
            self.url += self.dog_string
        if furniture == 1:
            self.url += self.furniture_string
        self.url += self.size_string+str(min_size)+"-"+str(max_size)
        self.url += self.cost_string+str(min_cost)+"-"+str(max_cost)
        print(self.url)

<<<<<<< HEAD
    def _pre_check(self):
        uri = self.index_url+'/oldal1.html'
        response = requests.get(uri)
        soup = bs4.BeautifulSoup(response.text)
        alert = soup.find('h4', attrs={'class': 'alert'})
        if alert == None:
            return True
        return False

    def get_urls(self):
        if (self._pre_check() == False):
            # search has found nothing
            return 0
        pageNum = 0
        while True:
            pageNum += 1
            print(pageNum)
            response = requests.get(self.index_url+"/oldal"+str(pageNum)+".html")
            soup = bs4.BeautifulSoup(response.text)
            # find the rent box div
            divs = soup.find_all('div', attrs={'class': 'main_normal_ad'})
            # print(divs)
            for div in divs:
                self.numberOflinks += 1
                #link = self.__get_link(div)
                #street = self.__get_address(div)
                #price = self.__get_price(div)
                #size = self.__get_area_size(div)
                #self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}
            print(str(self.numberOflinks))
            _next = soup.find('li', attrs={'class': 'last'})
            # no more page
            if _next == None:
                print("break")
                break

    def __get_link(self, div):
        address = div.find('div', attrs={'class': 'box-grid-head'})
        _link = address.find('a')['href']
        if _link.startswith('/'):
            return self.root_url + _link
        return _link
