# coding: utf-8

from source import Source


class LDLC(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        items = soup.find_all('div', attrs={'class': 'productWrapper'})
        for item in items:
            product_name = item.find('a', attrs={'class': 'designation'}).get('title')
            product_price = self.clean_price(item.find('span', attrs={'class': 'price'}).text)
            deals[product_name] = product_price

        items = soup.find_all('div', attrs={'class': 'swiper-slide'}) + soup.find_all('div', attrs={'class': 'details clearfix'})
        for item in items:
            txt_item = item.find('div', attrs={'class': 'txt'})
            if txt_item is None:
                continue
            anchor_item = txt_item.find('a')
            product_name = anchor_item.text
            product_price = self.clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price


# if __name__ == '__main__':
#     from loguru import logger
#     vendor = LDLC()
#     fetched_deals = vendor.fetch_deals()
#     for deal in fetched_deals:
#         logger.info(deal)
#     print(logger.info(fetched_deals))
