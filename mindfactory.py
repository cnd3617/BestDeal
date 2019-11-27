# coding: utf-8

from source import Source
from loguru import logger


class MindFactory(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def enrich_deals_from_soup(self, soup, deals):
        for product in soup.findAll('div', attrs={'class': 'pcontent'}):
            product_name = product.find('div', attrs={'class': 'pname'}).text
            product_price = product.find('div', attrs={'class': 'pprice'}).text
            deals[product_name] = self.clean_price(product_price)


# if __name__ == '__main__':
#     vendor = MindFactory()
#     fetched_deals = vendor.fetch_deals()
#     for deal in fetched_deals:
#         logger.info(deal)
#     logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
