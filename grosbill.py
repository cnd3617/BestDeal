# coding: utf-8

from vendor import Vendor


class GrosBill(Vendor):
    def __init__(self):
        sites = [
            'http://bit.do/eL5j9',  # GTX 1060 6GB
            'http://bit.do/eL5kj',  # GTX 1660 Ti
            'http://bit.do/eL5kA',  # RTX 2070
            'http://bit.do/eL5kH',  # RTX 2080
            'http://bit.do/eL5kP',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for product in soup.find('table', attrs={'id': 'listing_mode_display'}).findAll('tr'):
            try:
                product_name = product.find('div', attrs={'class': 'product_description'}).find('a').text
                product_price = self.clean_price(product.find('td', attrs={'class': 'btn_price_wrapper'}).find('b').text)
                deals[product_name] = product_price
            except:
                pass
