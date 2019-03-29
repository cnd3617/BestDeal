# coding: utf-8

from vendor import Vendor


class TopAchat(Vendor):
    def __init__(self):
        sites = [
            'http://bit.do/eL5BS',  # GTX 1060 6GB
            'http://bit.do/eL5B9',  # GTX 1660
            'http://bit.do/eL5Cr',  # GTX 1660 Ti
            'http://bit.do/eL5Cz',  # RTX 2060
            'http://bit.do/eL5CG',  # RTX 2070
            'http://bit.do/eL5CQ',  # RTX 2080
            'http://bit.do/eL5CU',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for item in soup.findAll('article', attrs={'class': 'grille-produit'}):
            product_name = item.find('h3').text
            product_price = self.clean_price(item.find('div', attrs={'itemprop': 'price'}).text)
            deals[product_name] = product_price
