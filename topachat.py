# coding: utf-8

from vendor import Vendor


class TopAchat(Vendor):
    def __init__(self):
        sites = [
            'https://bit.ly/2uBlMQz',  # GTX 1060 6GB
            'https://bit.ly/2FLwEld',  # GTX 1660
            'https://bit.ly/2uzOWiG',  # GTX 1660 Ti
            'https://bit.ly/2CMzlkr',  # RTX 2060
            'https://bit.ly/2FMNlg0',  # RTX 2070
            'https://bit.ly/2JQck65',  # RTX 2080
            'https://bit.ly/2TG5EXT',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for item in soup.findAll('article', attrs={'class': 'grille-produit'}):
            product_name = item.find('h3').text
            product_price = self.clean_price(item.find('div', attrs={'itemprop': 'price'}).text)
            deals[product_name] = product_price
