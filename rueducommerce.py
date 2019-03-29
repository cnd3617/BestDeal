# coding: utf-8

from vendor import Vendor


class RueDuCommerce(Vendor):
    def __init__(self):
        sites = [
            'http://bit.do/eL5iy',     # GTX 1060 6GB
            'http://bit.do/eL5iL',     # GTX 1660
            'http://bit.do/eL5iW',     # GTX 1660 Ti
            'http://bit.do/eL5gy',     # RTX 2070
            'http://bit.do/eL5gP',     # RTX 2080
            'https://bit.ly/2CCjB4b',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
            product_name = item.find('div', attrs={'class': 'summary'}).text
            product_price = self.clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price
