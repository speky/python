__author__ = 'speky'
import requests
import bs4
import operator
import base


class BudapestIngatlanSearch(base.BaseSearch):

    def __init__(self):
        base.BaseSearch.__init__(self)
        self.root_url = 'http://http://budapest.ingatlan.hu'
        self.index_url = self.root_url + '/kiado/lakas/'

    def set_params(self, min_cost, max_cost, min_size, max_size, dog, furniture, district):
        self.url = self.index_url
        if len(str(district)) > 0:
            self.url += self.__set_district(district)

        self.url += self.size_string+str(min_size)+"nm-tol;"+str(max_size)+"nm-ig"
        self.url += self.cost_string+str(min_cost)+"Eft-tol;"+str(max_cost)+"-Eft-ig"
        print(self.url)

    def __set_district(self, district):
        _result = ""
        _prefix = "budapest-"
        _postfix = "-ker"
        for num in district.split('+'):
            _result += _prefix + num + _postfix + '+'
        _result = _result[:-1]
        return _result+':'


    def get_urls(self):
         _lastPage = int(self.__get_max_page_number())
         #print("lastpage: "+str(_lastPage))
         for pageNumber in range(0, _lastPage):
             #print ("pageNumber: " + str(pageNumber))
             self.__get_page_urls(pageNumber)
         return self.numberOflinks

    def __get_page_urls(self, pageNum):
        response = requests.get(self.url+"?record="+str(pageNum*50)+"&num=50")
        soup = bs4.BeautifulSoup(response.text)
        # find the rent box div
        divs = soup.find_all('div', attrs={'class': 'result-row'})
        # print(divs)
        for div in divs:
            self.numberOflinks += 1
            link = self.__get_link(div)
            street = self.__get_address(div)
            price = self.__get_price(div)
            size = self.__get_area_size(div)
            self.rentHouses[link] = {'address': street, 'price': price, 'size': size, 'distance': 0}

    def __get_area_size(self, div):
        _p = div.find('div', attrs={'class': 'column'})
        _size = _p.text
        _size = ''.join(_size.split())
        # remove m2 string from the end
        _size = _size[:-2]
        return _size

    def __get_max_page_number(self):
        _response = requests.get(self.url)
        _soup = bs4.BeautifulSoup(_response.text)
        _max = _soup.find('div', attrs={'class': 'pages'})
        if (_max == None):
            return 1
        # get max page number
        _pageNum = _max.split('/')[-1]
        return _max.text[-5:]

    def __get_link(self, div):
        _link = div['data-url']
        if _link.startswith('/'):
            return self.root_url + _link
        return _link

    def __get_address(self, div):
        _address = div.find('div', attrs={'class': 'title'})
        return _address.strip()

    def __get_price(self, div):
        _price = div.find('div', attrs={'class': 'data'})
        #_price = ''.join(_price.split())
        # remove HUF string from the end
        _price = _price[:-2]
        return _price
