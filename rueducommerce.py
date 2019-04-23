# coding: utf-8

from vendor import Vendor
from loguru import logger


class RueDuCommerce(Vendor):
    def __init__(self):
        sites = [
            'https://bit.ly/2V4ev77',  # GTX 1060 6GB
            'https://bit.ly/2COCaRY',  # GTX 1660
            'https://bit.ly/2YAYzvs',  # GTX 1660 Ti
            'https://bit.ly/2UsWLWl',  # RTX 2070
            'https://bit.ly/2U5ZHsw',  # RTX 2080
            'https://bit.ly/2CCjB4b',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
            product_name = item.find('div', attrs={'class': 'summary'}).text
            product_price = self.clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price


if __name__ == '__main__':
    vendor = RueDuCommerce()
    fetched_deals = vendor.fetch_deals()
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
