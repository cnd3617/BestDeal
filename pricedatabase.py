# coding: utf-8

from pymongo import MongoClient
from loguru import logger
from datetime import datetime, timezone


class PriceDatabase:
    """
    Powered by MongoDB <3
    """

    def __init__(self, host, port, collection_name):
        self.database_name = "PriceHistorization"
        logger.info('Connecting to database [{}]'.format(self.database_name))
        self.client = MongoClient(host, port)
        self.database = self.client[self.database_name]
        self.collection = self.database[collection_name]

    @staticmethod
    def get_today_date():
        return datetime.now(timezone.utc).strftime('%Y%m%d')

    @staticmethod
    def get_today_datetime():
        return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')

    def bulk_insert(self, posts):
        logger.debug(f"Inserting [{len(posts)}] posts")
        result = self.collection.insert_many(posts)
        logger.debug(result)
