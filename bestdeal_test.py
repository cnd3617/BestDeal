# coding: utf-8

import unittest
from bestdeal import BestDeal


class TestBestDeal(unittest.TestCase):
    def setUp(self):
        pass

    def test_find_exactly_one_element(self):
        brands = ["GAINWARD", "ASUS"]
        product_data = "6GB Gainward GeForce GTX 1660 Pegasus OC Aktiv PCIe 3.0 x16 (Retail)"
        result = BestDeal.find_exactly_one_element(pattern_data=brands, raw_data=product_data)
        self.assertIsNotNone(result, "GAINWARD brand should be found")
