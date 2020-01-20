# coding: utf-8

from source import Source
from toolbox import clean_price


class RueDuCommerce(Source):
    """
    https://uselesscsp.com/rue-du-commerce.html
    TLDR: it doesn't work
    """
    def __init__(self):
        sites = []
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        # logger.debug(soup.prettify())
        for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
            product_name = item.find('div', attrs={'class': 'summary'}).text
            product_price = clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price


# if __name__ == '__main__':
#     vendor = RueDuCommerce()
#     fetched_deals = vendor.fetch_deals()
#     for deal in fetched_deals:
#         logger.info(deal)
#     logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
