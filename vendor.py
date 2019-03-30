# coding: utf-8

import re
import bs4
import requests


class Vendor:
    def __init__(self, source_name, sites):
        self.source_name = source_name
        self.sites = sites
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                                      '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    def fetch_deals(self):
        deals = {}
        for site in self.sites:
            html = requests.get(url=site, headers=self.headers)
            soup = bs4.BeautifulSoup(html.text, 'html.parser')
            self.enrich_deals_from_soup(soup, deals)
        return deals

    @staticmethod
    def clean_price(dirty_price):
        """
        Clean the price to facilitate comparisons
        """
        dirty_price = dirty_price.replace(' ', '')
        m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
        return '{}.{}'.format(m.group(1), m.group(2))

    def enrich_deals_from_soup(self, soup, deals):
        raise NotImplementedError()
