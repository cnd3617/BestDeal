# coding: utf-8

import pricedatabase
import time
from topachat import TopAchat
from grosbill import GrosBill
from rueducommerce import RueDuCommerce
from cybertek import Cybertek
from ldlc import LDLC
from loguru import logger
from collections import namedtuple


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
            except AttributeError as exception:
                logger.exception(exception)
            except Exception as exception:
                logger.exception(exception)
            logger.info('Waiting [{}] seconds until next deal watch'.format(self.wait_in_seconds))
            time.sleep(self.wait_in_seconds)

    def extract_product_type(self, product_name):
        product_type = None
        for model in self.product_types:
            if model in product_name:
                product_type = model
                break
        if product_type and (' ti' in product_name.lower() or 'ti ' in product_name.lower() or '0ti' in product_name.lower()):
            # Product 1060 Ti does not exist...
            if product_type != '1060':
                product_type += ' Ti'
        return product_type

    def display_best_deals(self):
        logger.info('Best deals for [{}]'.format(self.db.get_today_date()))
        cheapest_products = []
        for product_type in self.db.get_all_product_types():
            cheapest = self.db.get_cheapest(product_type, self.db.get_today_date())
            if cheapest is not None:
                cheapest_products.append(cheapest)
        max_lengths = {}
        for product in cheapest_products:
            for key, value in product.items():
                max_lengths.setdefault(key, 0)
                max_lengths[key] = max(max_lengths[key], len(str(value)))
        for product in cheapest_products:
            template = 'Cheapest [{product_type:' + str(max_lengths['product_type']) + '}] [{histo_price:' + str(max_lengths['histo_price']) + '}]€ [{product_name:' + str(max_lengths['product_name']) + '}] [{source_name:' + str(max_lengths['source_name']) + '}]'
            logger.info(template.format(**product))

    def scrap_and_store(self):
        sources = [TopAchat(),
                   GrosBill(),
                   RueDuCommerce(),
                   Cybertek(),
                   LDLC()]
        for source in sources:
            logger.info('Fetch deals from [{}]'.format(source.source_name))
            try:
                deals = source.fetch_deals()
            except Exception as exception:
                logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.source_name, exception))
                continue
            update_price_details = []
            for product_name, product_price in deals.items():
                product_type = self.extract_product_type(product_name)
                if product_type:
                    update_price_detail = self.update_price(product_name, product_type, source.source_name, float(product_price))
                    if update_price_detail is not None:
                        update_price_details.append(update_price_detail)
                else:
                    logger.debug('Ignoring [{}]'.format(product_name))
            if update_price_details:
                self.format_log_update_price_details(update_price_details)

    @staticmethod
    def format_log_update_price_details(update_price_details):
        """
        Bloat code to fit to maximum length
        TODO: refactor this
        """
        product_name_max_length = 0
        source_name_max_length = 0
        new_price_max_length = 0
        today_last_price_max_length = 0
        for detail in update_price_details:
            product_name_max_length = max(product_name_max_length, len(detail.product_name))
            source_name_max_length = max(source_name_max_length, len(detail.source_name))
            new_price_max_length = max(new_price_max_length, len(detail.new_price))
            if detail.today_last_price is not None:
                today_last_price_max_length = max(today_last_price_max_length, len(detail.today_last_price))
        template = 'New price for [{:' + str(product_name_max_length) + '}] from [{:' + str(source_name_max_length) + '}] : [{:' + str(new_price_max_length) + '}]{}'
        for detail in update_price_details:
            previous_price_info = ''
            if detail.today_last_price is not None:
                previous_price_info = ' Today last price [{:' + str(today_last_price_max_length) + '}]'.format(detail.today_last_price)
            logger.info(template.format(detail.product_name, detail.source_name, detail.new_price, previous_price_info))

    def update_price(self, product_name, product_type, source_name, new_price):
        source_id = self.db.insert_if_necessary(table='source',
                                                columns=['source_name'],
                                                values=[source_name])
        product_id = self.db.insert_if_necessary(table='product',
                                                 columns=['product_name', 'product_type'],
                                                 values=[product_name, product_type])
        today_last_price = self.db.get_last_price_for_today(product_id, source_id)
        update_price_details = None
        UpdatePriceDetails = namedtuple('UpdatePriceDetails', 'product_name source_name new_price today_last_price')
        if today_last_price is None or today_last_price != new_price:
            self.db.add_price(product_id, source_id, new_price, self.db.get_today_datetime())
            update_price_details = UpdatePriceDetails(product_name, source_name, str(new_price), str(today_last_price) if today_last_price else None)
        return update_price_details


if __name__ == '__main__':
    bd = BestDeal()
    bd.continuous_watch()
