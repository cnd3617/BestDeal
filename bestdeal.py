# coding: utf-8

import sys
import pricedatabase
import logging
import dealscrappers
import time
import itertools


class BestDeal:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = pricedatabase.PriceDatabase()
        self.product_types = ['1070', '1080', '2060', '2070', '2080']

    def continuous_watch(self):
        wait_in_seconds = 900
        while True:
            self.record_best_deals()
            self.display_best_deals()
            self.logger.info('Waiting [{}] seconds until next deal watch'.format(wait_in_seconds))
            time.sleep(wait_in_seconds)

    def extract_product_type(self, product_name):
        product_type = None
        for model in self.product_types:
            if model in product_name:
                product_type = 'GTX ' + model
                break
        if product_type and (' ti' in product_name.lower() or 'ti ' in product_name.lower() or '0ti' in product_name.lower()):
            product_type += ' Ti'
        return product_type

    def display_best_deals(self):
        # histo_date = self.db.get_today_date()
        # self.logger.info('Best deals for [{}]'.format(histo_date))
        # product_items = [['GTX'], self.product_types, ['', 'Ti']]
        # for element in itertools.product(*product_items):
        #     product_type = ' '.join(element).strip()
        #     cheapest_product = self.db.get_cheapest_price_from_all_sources(product_type=product_type, histo_date=histo_date)
        #     if cheapest_product[0]['product_name']:
        #         cheapest_product[0]['product_type'] = product_type
        #         self.logger.info(
        #             'Cheapest [{product_type:11}] [{histo_price:7}]€ [{product_name:115}] [{source_name:13}]'.format(**cheapest_product[0]))
        cheapest_products = self.db.get_cheapest_by_product_type()
        self.logger.info('Best deals for [{}]'.format(self.db.get_today_date()))
        for product in cheapest_products:
            self.logger.info('Cheapest [{product_type:11}] [{histo_price:7}]€ [{product_name:115}] [{source_name:13}]'.format(**product))

    def record_best_deals(self):
        sources = [dealscrappers.TopAchat,
                   dealscrappers.GrosBill,
                   dealscrappers.RueDuCommerce,
                   dealscrappers.Cybertek]
        for source in sources:
            self.logger.info('Fetch deals from [{}]'.format(source.__name__))
            deals = source.fetch_deals()
            for product_name, product_price in deals.items():
                product_type = self.extract_product_type(product_name)
                if product_type:
                    self.update_price(product_name, product_type, source.__name__, float(product_price))
                else:
                    self.logger.debug('Ignoring [{}]'.format(product_name))

    def update_price(self, product_name, product_type, source_name, new_price):
        source_id = self.db.insert_if_necessary(table='source',  columns=['source_name'], values=[source_name])
        product_id = self.db.insert_if_necessary(table='product', columns=['product_name', 'product_type'], values=[product_name, product_type])
        today_last_price = self.db.get_last_price_for_today(product_id, source_id)
        if today_last_price is None or today_last_price != new_price:
            previous_price_info = 'Today last price [{:7}]'.format(today_last_price) if today_last_price else ''
            self.logger.info('New price for [{:115}] from [{:13}] : [{:7}] {}'.format(product_name, source_name, new_price, previous_price_info))
            self.db.add_price(product_id, source_id, new_price, self.db.get_today_datetime())


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S %p')

    bd = BestDeal()
    bd.continuous_watch()
    # bd.display_best_deals()
