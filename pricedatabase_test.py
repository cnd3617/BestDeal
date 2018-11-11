import unittest
import pricedatabase
from datetime import datetime, timezone, timedelta


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = pricedatabase.PriceDatabase(filename=':memory:')

    def feed_database(self, source_name, product_name, product_type, prices):
        source_id = self.db.insert_if_necessary(table='source', columns=['source_name'], values=[source_name])
        product_id = self.db.insert_if_necessary(table='product', columns=['product_name', 'product_type'], values=[product_name, product_type])
        for price in prices:
            self.datetimestamp += timedelta(minutes=1)
            self.db.add_price(product_id, source_id, price, self.datetimestamp.strftime('%Y%m%d_%H%M%S'))

    def test_00_get_cheapest_price(self):
        """
        Validate we get minimum price for a given:
        - day
        - source
        - product type
        """
        self.datetimestamp = datetime.now(timezone.utc)
        # Add prices for today (1 minute spaced for each price record)
        self.feed_database('Source1', 'Product1', 'GTX 1080', [15.0, 80, 120]) # Good answer : 15
        self.feed_database('Source1', 'Product2', 'GTX 1080', [50, 30, 75])
        self.feed_database('Source1', 'Product3', 'GTX 1080', [1000.0, 390, 50])
        self.feed_database('Source1', 'Product4', 'GTX 1070', [1, 200, 79]) # Wrong product type
        self.feed_database('Source1', 'Product5', 'GTX 1070', [100, 200, 75])
        self.feed_database('Source2', 'Product6', 'GTX 1080', [2, 95, 42]) # Wrong source
        # Add prices for yesterday
        self.datetimestamp -= timedelta(days=1)
        self.feed_database('Source3', 'Product1', 'GTX 1080', [3, 500, 350]) # Wrong date
        self.feed_database('Source1', 'Product1', 'GTX 1080', [4, 500, 350]) # Wrong date
        self.feed_database('Source2', 'Product1', 'GTX 1080', [5, 500, 350]) # Wrong date

        self.datetimestamp += timedelta(days=1)
        source_id = self.db.insert_if_necessary(table='source', columns=['source_name'], values=['Source1'])

        result = self.db.get_cheapest_price(source_id, 'GTX 1080', self.datetimestamp.strftime('%Y%m%d'))
        self.assertEqual(len(result), 1) # Only 1 record
        self.assertEqual(result[0]['histo_price'], 15.0) # Exact minimum price
        self.assertEqual(result[0]['product_name'], 'Product1') # Exact product name


if __name__ == '__main__':
    unittest.main()
