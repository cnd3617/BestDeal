# coding: utf-8

import re
import time
from pricedatabase import PriceDatabase
from abc import ABCMeta, abstractmethod
from source import Source
from typing import Optional, Dict, Tuple
from collections import namedtuple
from loguru import logger
from toolbox import get_today_date
from toolbox import get_today_datetime


class AbstractFetcher:
    __metaclass__ = ABCMeta

    def __init__(self, database: PriceDatabase):
        self.wait_in_seconds = 900
        self.database = database

    @abstractmethod
    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        pass

    @abstractmethod
    def _extract_product_data(self, product_description) -> Tuple[Optional[str], Optional[str]]:
        pass

    def continuous_watch(self):
        while 1:
            try:
                self._scrap_and_store()
                self._display_best_deals()
            except KeyboardInterrupt:
                logger.info("Stopping gracefully...")
                break
            except Exception as exception:
                logger.exception(exception)

            try:
                logger.info('Waiting [{}] seconds until next deal watch'.format(self.wait_in_seconds))
                time.sleep(self.wait_in_seconds)
            except KeyboardInterrupt:
                logger.info("Stopping gracefully...")
                break

    def _scrap_and_store(self):
        """
        Example:
        source_class = TopAchat
        product_url_mapping = {'1660 SUPER': 'https://bit.ly/2CJDkOi'}
        """

        posts = []
        for source_class, product_url_mapping in self.get_source_product_urls().items():
            logger.debug(f"Processing source [{source_class}]")
            source = source_class()

            # Scrap every available products for current source
            for product, url in product_url_mapping.items():
                deals = self._scrap_product(source, product, url)
                if not deals:
                    continue

                # Create posts to insert in mongodb
                for product_name, product_price in deals.items():
                    brand, product_type = self._extract_product_data(product_name)
                    if product_type:
                        last_price = None
                        last_update = self.database.find_last_price(product_name, get_today_date())
                        if last_update:
                            last_price = last_update["product_price"]
                            if last_price == float(product_price):
                                continue

                        logger.info(f"New price for [{product_name}] [{product_price}] (previous [{last_price}])")

                        post = {"product_name": product_name,
                                "product_brand": brand,
                                "product_type": product_type,
                                "product_price": float(product_price),
                                "source": source.source_name,
                                "url": url,
                                "timestamp": get_today_datetime()}
                        posts.append(post)
                        #logger.info(post)

        if self.database and posts:
            self.database.bulk_insert(posts)

            # deals = self._scrap(source, product_url_mapping)
            # update_price_details = self._store(source, deals)
            # if update_price_details:
            #     self._format_log_update_price_details(update_price_details)

    def _scrap_product(self, source: Source, product, url):
        """
        Fetch deals for ONE product (one url)
        """
        deals = None
        logger.info(f'Fetch [{product}] deals from [{source.source_name}]')
        try:
            deals = source.fetch_deals(product, url)
        except Exception as exception:
            logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.source_name, exception))
        return deals

    def _update_price(self, product_name, product_type, source_name, new_price):

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
            self.db.add_price(product_id, source_id, new_price, get_today_datetime())
            update_price_details = UpdatePriceDetails(product_name, source_name, str(new_price), str(today_last_price) if today_last_price else None)
        return update_price_details

    def _display_best_deals(self):
        today_date = get_today_date()
        logger.info(f"Best deals for [{today_date}]")
        cheapest_products = []
        for product_type in self.database.find_distinct_product_types():
            cheapest = self.database.find_cheapest(product_type, today_date)
            if cheapest is not None:
                cheapest_products.append(cheapest)
        max_lengths = {}
        for product in cheapest_products:
            for key, value in product.items():
                max_lengths.setdefault(key, 0)
                max_lengths[key] = max(max_lengths[key], len(str(value)))
        for product in cheapest_products:
            template = 'Cheapest [{product_type:' + str(max_lengths['product_type']) + '}] ' \
                       '[{product_price:' + str(max_lengths['product_price']) + '}]€' \
                       '[{product_name:' + str(max_lengths['product_name']) + '}] ' \
                       '[{source:' + str(max_lengths['source']) + '}]'
            logger.info(template.format(**product))

    @staticmethod
    def find_exactly_one_element(pattern_data, raw_data) -> Optional[str]:
        """
        Search a pattern_data among raw_data
        Examples:

        """
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
    def _format_log_update_price_details(update_price_details):
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
        template = 'New price for [{:' + str(product_name_max_length) + '}] from [{:' + str(
            source_name_max_length) + '}] : [{:' + str(new_price_max_length) + '}]{}'
        for detail in update_price_details:
            previous_price_info = ''
            if detail.today_last_price is not None:
                previous_price_info = ' Today last price [{:' + str(today_last_price_max_length) + '}]'
                previous_price_info.format(detail.today_last_price)
            logger.info(template.format(detail.product_name, detail.source_name, detail.new_price, previous_price_info))
