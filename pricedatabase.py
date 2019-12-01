# coding: utf-8

from pymongo import MongoClient, ASCENDING
from loguru import logger


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

    def bulk_insert(self, posts):
        logger.debug(f"Inserting [{len(posts)}] posts")
        result = self.collection.insert_many(posts)
        logger.debug(result)

    def find_cheapest(self, product_type):
        """
        TODO: fix method, filter on timestamp doesn't seem to work well
        in MongoShell, this works:
        > db.NVidiaGPU.find({"product_type": "2060", "timestamp": /20191130_/}).sort({product_price: 1}).limit(1)
        """
        f = self.collection.find({"product_type": product_type})
        # f = self.collection.find({"product_type": product_type, "timestamp": f"/{self.get_today_date()}_/"})
        s = f.sort("product_price", ASCENDING)  # ascending price
        for post in s.limit(1):
            logger.info(post)
