# coding: utf-8

import re
import pricedatabase
import time
from typing import Optional
from topachat import TopAchat
from grosbill import GrosBill
from rueducommerce import RueDuCommerce
from cybertek import Cybertek
from ldlc import LDLC
from mindfactory import MindFactory
from loguru import logger
from collections import namedtuple


class BestDeal:
    def __init__(self, in_memory=False):
        self.wait_in_seconds = 900
        self.database_filename = 'PricesHistorization.db'
        if in_memory:
            self.database_filename = ':memory:'
        self.db = pricedatabase.PriceDatabase(self.database_filename)
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

    @staticmethod
    def find_exactly_one_element(pattern_data, raw_data) -> Optional[str]:
        result = None
        refined_pattern_tokens = []
        at_least_one_space = r'\s{1,}'
        # Build search pattern for " Tixxx" or "2070SUPER " (there must be at least one space)
        # Avoid to gather "xxxxxTIxxxx"
        for pattern_token in pattern_data:
            refined_pattern_tokens.append(f'{at_least_one_space}{pattern_token}')
            refined_pattern_tokens.append(f'{pattern_token}{at_least_one_space}')
        pattern = r"{}".format('|'.join(refined_pattern_tokens))
        parsed = re.findall(pattern, raw_data, re.IGNORECASE)
        parsed = list(set(map(lambda x: x.strip().upper(), parsed)))
        if len(parsed) > 1:
            logger.warning(f'Parsed data is wrong [{parsed}]')
        elif parsed:
            result = parsed[0]
        return result

    @staticmethod
    def extract_product_data(product_description):
        brands = [
            'GAINWARD',
            'KFA2',
            'GIGABYTE',
            'ZOTAC',
            'MSI',
            'PNY',
            'PALIT',
            'EVGA',
            'ASUS',
            'INNO3D',
        ]
        lineup_type = ['TI', 'SUPER']
        product_classes = ['1050', '1060', '1660', '1070', '1080', '2060', '2070', '2080']
        higher_lineup = {
            'TI': ['1050', '1660', '2080'],
            'SUPER': ['1660', '2060', '2070', '2080']
        }
        standard_lineup = ['1050', '1060', '1070', '1080', '1660', '2060', '2070', '2080']

        brand = BestDeal.find_exactly_one_element(brands, product_description)
        if not brand:
            logger.warning(f'Brand not found in product [{product_description}]')
            return None, None

        lineup_type_result = BestDeal.find_exactly_one_element(lineup_type, product_description)
        product_class = BestDeal.find_exactly_one_element(product_classes, product_description)

        product_type = None
        if lineup_type_result and product_class in higher_lineup[lineup_type_result] or product_class in standard_lineup:
            product_type = product_class

        if product_type is not None and lineup_type_result is not None:
            product_type += f' {lineup_type_result}'

        return brand, product_type

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
            template = 'Cheapest [{product_type:' + str(max_lengths['product_type']) + '}] ' \
                       '[{histo_price:' + str(max_lengths['histo_price']) + '}]€' \
                       '[{product_name:' + str(max_lengths['product_name']) + '}] ' \
                       '[{source_name:' + str(max_lengths['source_name']) + '}]'
            logger.info(template.format(**product))

    def scrap_and_store(self):
        sources = [
            TopAchat(),
            GrosBill(),
            RueDuCommerce(),
            Cybertek(),
            LDLC(),
            MindFactory()
        ]
        for source in sources:
            logger.info('Fetch deals from [{}]'.format(source.source_name))
            try:
                deals = source.fetch_deals()
            except Exception as exception:
                logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.source_name, exception))
                continue
            update_price_details = []
            for product_description, product_price in deals.items():
                brand, product_type = self.extract_product_data(product_description)
                if product_type:
                    update_price_detail = self.update_price(product_description, product_type, source.source_name, float(product_price))
                    if update_price_detail is not None:
                        update_price_details.append(update_price_detail)
                else:
                    logger.debug(f'Ignoring [{product_description}]')
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
                previous_price_info = ' Today last price [{:' + str(today_last_price_max_length) + '}]'
                previous_price_info.format(detail.today_last_price)
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
