# coding: utf-8

import re
import time
from pricedatabase import PriceDatabase
from abc import ABCMeta, abstractmethod
from source import Source
from typing import Optional, Dict, Tuple
from loguru import logger
from toolbox import get_today_date
from toolbox import get_today_datetime


class AbstractFetcher:
    __metaclass__ = ABCMeta

    def __init__(self, database: Optional[PriceDatabase]):
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
                logger.info(f"Waiting [{self.wait_in_seconds}] seconds until next deal watch")
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

        if self.database is None:
            logger.warning("Database is not available.")
            return

        posts = []
        for source_class, product_url_mapping in self._get_source_product_urls().items():
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

        if posts:
            self.database.bulk_insert(posts)
        else:
            logger.info("Nothing to insert")

    def _scrap_product(self, source: Source, product: str, url: str) -> Dict[str, str]:
        """
        Fetch deals for ONE product (one url)
        :return: Dict["product_name"] = "product_price"
        """
        deals = None
        logger.info(f'Fetch [{product}] deals from [{source.source_name}]')
        try:
            deals = source.fetch_deals(product, url)
        except Exception as exception:
            logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.source_name, exception))
        return deals

    def _display_best_deals(self) -> None:
        if self.database is None:
            logger.warning("Database is not available.")
            return

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
