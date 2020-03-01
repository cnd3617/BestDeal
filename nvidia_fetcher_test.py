# coding: utf-8

import unittest
from nvidia_fetcher import NVidiaFetcher


class TestFindExactlyOneElement(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = NVidiaFetcher(":in_memory:")

    @unittest.skip("TODO")
    def test_case_1(self):
        brands = ["GAINWARD", "ASUS"]
        product_data = "6GB Gainward GeForce GTX 1660 Pegasus OC Aktiv PCIe 3.0 x16 (Retail)"
        result = self.fetcher.find_exactly_one_element(pattern_data=brands, raw_data=product_data)
        self.assertIsNotNone(result, "GAINWARD brand should be found")


class TestExtractProductData(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = NVidiaFetcher(":in_memory:")

    def test_case_1(self):
        product_description = 'Palit GeForce GTX 1660 Ti StormX, 6 Go'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('PALIT', brand)
        self.assertEqual('1660 TI', product_type)

    def test_case_2(self):
        product_description = 'Zotac Gaming GeForce GTX 1060 AMP Edition, 6 Go + jeu offert ! '
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('ZOTAC', brand)
        self.assertEqual('1060', product_type)

    def test_case_3(self):
        product_description = 'MSI 2060 SuPeR'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('MSI', brand)
        self.assertEqual('2060 SUPER', product_type)

    def test_case_4(self):
        product_description = 'GIGABYTE GeForce® GTX  1050TI D5 4G'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('GIGABYTE', brand)
        self.assertEqual('1050 TI', product_type)

    def test_case_5(self):
        product_description = 'MSI RTX 3080 Ti 6 Go'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('MSI', brand)
        self.assertEqual('3080 TI', product_type)

    def test_case_6(self):
        product_description = 'RTX 3070 GAINWARD'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('GAINWARD', brand)
        self.assertEqual('3070', product_type)

    def test_case_7(self):
        product_description = 'RTX PNY 3080'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('PNY', brand)
        self.assertEqual('3080', product_type)
