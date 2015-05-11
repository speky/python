__author__ = 'ezsospe'


class BaseSearch():
    def __init__(self):
        self.url = ""
        self.numberOflinks = 0

    def set_params(self, min_cost, max_cost, min_size, max_size, kisallat, butor, kerulet):
        self.url = str(min_cost) + str(max_cost) + str(min_size) +  str(max_size) + str(kisallat) + str(butor) + str(kerulet)
        print(self.url)

    def get_page_urls(self):
        return self.numberOflinks
