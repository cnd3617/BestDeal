# coding: utf-8

import re
from vendor import Vendor
from loguru import logger


class Cybertek(Vendor):
    def __init__(self):
        sites = [
            'https://bit.ly/2OyuckC',  # GTX 1060 6GB
            'https://bit.ly/2uL1bJH',  # GTX 1660
            'https://bit.ly/2YHhJjx',  # GTX 1660 Ti
            'https://bit.ly/2OITRYd',  # RTX 2060
            'https://bit.ly/2FElIo5',  # RTX 2070
            'https://bit.ly/2TIQ4uM',  # RTX 2080
            'https://bit.ly/2JSMgaD',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    @staticmethod
    def remove_garbage_characters(string):
        return string.replace('\r', '').replace('\n', '').replace('\t', '')

    @staticmethod
    def remove_all_span(tag):
        for span_tag in tag.findAll('span'):
            span_tag.replace_with('')

    def enrich_deals_from_soup(self, soup, deals):
        # logger.info(soup.prettify())
        products = soup.findAll('div', attrs={'class': re.compile('ppp-*')})
        for product in products:
            tag = product.find('div', attrs={'class': re.compile('product*')})
            brand = tag.find('span', attrs={'class': 'marque'}).text
            self.remove_all_span(tag)
            second_part = tag.find('a', attrs={'class': 'prod_txt_left'}).text
            product_name = brand + self.remove_garbage_characters(second_part)
            product_price = self.clean_price(product.find('div', attrs={'class': 'price_prod_resp'}).text)
            deals[product_name] = product_price


if __name__ == '__main__':
    vendor = Cybertek()
    fetched_deals = vendor.fetch_deals()
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
