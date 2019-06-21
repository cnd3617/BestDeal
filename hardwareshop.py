# coding: utf-8

import re
from vendor import Vendor


class HardwareShop(Vendor):
    def __init__(self):
        raise NotImplementedError()
        sites = [
            'XXXXXXXXXXXXXXXXXXXXXX',  # GTX 1060 6GB
            'XXXXXXXXXXXXXXXXXXXXXX',  # GTX 1660
            'XXXXXXXXXXXXXXXXXXXXXX',  # GTX 1660 Ti
            'XXXXXXXXXXXXXXXXXXXXXX',  # RTX 2060
            'XXXXXXXXXXXXXXXXXXXXXX',  # RTX 2070
            'XXXXXXXXXXXXXXXXXXXXXX',  # RTX 2080
            'XXXXXXXXXXXXXXXXXXXXXX',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        items = soup.find_all('li', attrs={'data-ref': re.compile("[A-Za-z0-9]")})
        for item in items:
            product_name = item.find('div', attrs={'class': 'description'}).find('h2').text
            for script_section in soup.findAll('script'):
                if '.price-wrapper' in script_section.text:
                    print(script_section.prettify())
            product_price = self.clean_price(item.find('div', attrs={'class': 'price_prod_resp'}).text)
            deals[product_name] = product_price
