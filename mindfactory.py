# coding: utf-8

from source import Source
from loguru import logger


class MindFactory(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        for product in soup.findAll('div', attrs={'class': 'pcontent'}):
            product_name = product.find('div', attrs={'class': 'pname'}).text
            product_price = product.find('div', attrs={'class': 'pprice'}).text
            deals[product_name] = self.clean_price(product_price)
