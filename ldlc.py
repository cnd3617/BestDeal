# coding: utf-8

from vendor import Vendor


# TODO: url are set, parse to be done
class LDLC(Vendor):
    def __init__(self):
        sites = [
            'https://bit.ly/2BrQrDN',  # GTX 1060
            'https://bit.ly/2D4e7hd',  # RTX 2080
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
            product_name = item.find('div', attrs={'class': 'summary'}).text
            product_price = self.clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price
