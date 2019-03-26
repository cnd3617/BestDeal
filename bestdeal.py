# coding: utf-8

import pricedatabase
import dealscrappers
import time
from loguru import logger


class BestDeal:
    def __init__(self):
        self.wait_in_seconds = 900
        self.db = pricedatabase.PriceDatabase()
        self.product_types = ['1060', '1660', '1070', '1080', '2060', '2070', '2080']

    def continuous_watch(self):
        while True:
            try:
                self.scrap_and_store()
                self.display_best_deals()
            except Exception as exception:
                logger.warning(exception)
            logger.info('Waiting [{}] seconds until next deal watch'.format(self.wait_in_seconds))
            time.sleep(self.wait_in_seconds)

    def extract_product_type(self, product_name):
        product_type = None
        for model in self.product_types:
            if model in product_name:
                product_type = model
                break
        if product_type and (' ti' in product_name.lower() or 'ti ' in product_name.lower() or '0ti' in product_name.lower()):
            product_type += ' Ti'
        return product_type

    def display_best_deals(self):
        cheapest_products = self.db.get_cheapest_by_product_type()
        logger.info('Best deals for [{}]'.format(self.db.get_today_date()))
        for product in cheapest_products:
            logger.info('Cheapest [{product_type:7}] [{histo_price:7}]€ [{product_name:115}] [{source_name:13}]'.format(**product))

    def scrap_and_store(self):
        sources = [dealscrappers.TopAchat,
                   dealscrappers.GrosBill,
                   dealscrappers.RueDuCommerce,
                   dealscrappers.Cybertek]
        for source in sources:
            logger.info('Fetch deals from [{}]'.format(source.__name__))
            try:
                deals = source.fetch_deals()
            except Exception as exception:
                logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.__name__, exception))
                continue
            for product_name, product_price in deals.items():
                product_type = self.extract_product_type(product_name)
                if product_type:
                    self.update_price(product_name, product_type, source.__name__, float(product_price))
                else:
                    logger.debug('Ignoring [{}]'.format(product_name))

    def update_price(self, product_name, product_type, source_name, new_price):
        source_id = self.db.insert_if_necessary(table='source',  columns=['source_name'], values=[source_name])
        product_id = self.db.insert_if_necessary(table='product', columns=['product_name', 'product_type'], values=[product_name, product_type])
        today_last_price = self.db.get_last_price_for_today(product_id, source_id)
        if today_last_price is None or today_last_price != new_price:
            previous_price_info = 'Today last price [{:7}]'.format(today_last_price) if today_last_price else ''
            logger.info('New price for [{:115}] from [{:13}] : [{:7}] {}'.format(product_name, source_name, new_price, previous_price_info))
            self.db.add_price(product_id, source_id, new_price, self.db.get_today_datetime())


if __name__ == '__main__':
    bd = BestDeal()
    bd.continuous_watch()
