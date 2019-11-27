# coding: utf-8

import unittest
from vendor import Source


class TestCleanPrice(unittest.TestCase):
    def setUp(self):
        self.reference_price = '422.45'

    def test_case_1(self):
        self.assertEqual(self.reference_price, Source.clean_price('      422.45   €*'))

    def test_case_2(self):
        self.assertEqual(self.reference_price, Source.clean_price('   ---   422,45   €*'))

    def test_case_3(self):
        self.assertEqual(self.reference_price, Source.clean_price('422€45'))

    def test_case_4(self):
        self.assertEqual(self.reference_price, Source.clean_price('4 22€45'))
