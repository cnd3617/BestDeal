# coding: utf-8

from vendor import Vendor


class LDLC(Vendor):
    def __init__(self):
        sites = [
            'https://bit.ly/2BrQrDN',  # GTX 1060 6GB
            'https://bit.ly/2HPijWU',  # GTX 1660
            'https://bit.ly/2uB0lPn',  # GTX 1660 Ti
            'https://bit.ly/2YAhVkl',  # RTX 2060
            'https://bit.ly/2uCuzBw',  # RTX 2070
            'https://bit.ly/2D4e7hd',  # RTX 2080
            'https://bit.ly/2HN8V6b',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
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


if __name__ == '__main__':
    from loguru import logger
    vendor = LDLC()
    deals = vendor.fetch_deals()
    for deal in deals:
        logger.info(deal)
    print(logger.info(deals))
