# coding: utf-8

from abstract_fetcher import AbstractFetcher
from topachat import TopAchat
from grosbill import GrosBill
from rueducommerce import RueDuCommerce
from cybertek import Cybertek
from ldlc import LDLC
from mindfactory import MindFactory
from loguru import logger
from typing import Dict
from source import Source


class NVidiaFetcher(AbstractFetcher):
    def __init__(self):
        super().__init__(collection_name='NVidiaGPU')

    def get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        return {
            TopAchat: {
                '1660 SUPER': 'https://bit.ly/2CJDkOi',
                '1660': 'https://bit.ly/2FLwEld',
                '1660 TI': 'https://bit.ly/2uzOWiG',
                '2060': 'https://bit.ly/2CMzlkr',
                '2070': 'https://bit.ly/2FMNlg0',
                '2080': 'https://bit.ly/2JQck65',
                '2060 Super': 'https://bit.ly/2Y1r2NL',
                '2070 Super': 'https://bit.ly/2YRb8Tj',
                '2080 Super': 'https://bit.ly/2Yp0AJT',
                '2080 TI': 'https://bit.ly/2TG5EXT'
            },
            GrosBill: {
                'Multiple products': 'https://bit.ly/2McijjE'
            },
            RueDuCommerce: {
            },
            Cybertek: {
                '1060 6GB': 'https://bit.ly/2OyuckC',
                '1660': 'https://bit.ly/2uL1bJH',
                '1660 TI': 'https://bit.ly/2YHhJjx',
                '1660 SUPER': 'https://bit.ly/2OMkPyq',
                '2060': 'https://bit.ly/2OITRYd',
                '2060 SUPER': 'https://bit.ly/2OSyMe2',
                '2070': 'https://bit.ly/2FElIo5',
                '2070 SUPER': 'https://bit.ly/2rzczcX',
                '2080': 'https://bit.ly/2TIQ4uM',
                '2080 SUPER': 'https://bit.ly/2qOGE8y',
                '2080 Ti': 'https://bit.ly/2JSMgaD',
            },
            LDLC: {
                '1660': 'https://bit.ly/2HPijWU',
                '1660 Ti': 'https://bit.ly/2uB0lPn',
                '2060': 'https://bit.ly/2YAhVkl',
                '2070': 'https://bit.ly/2uCuzBw',
                '2080': 'https://bit.ly/2D4e7hd',
                '2080 Ti': 'https://bit.ly/2HN8V6b',
            },
            MindFactory: {
                '1660': 'https://bit.ly/2QSN019',
                '1660 TI': 'https://bit.ly/2KXXWHk',
                '2060': 'https://bit.ly/2smzDw7',
                '2070': 'https://bit.ly/2DnaWlA',
                '2080': 'https://bit.ly/33kaTRP',
                '2080 TI': 'https://bit.ly/35EpY2h',
            }
        }

    def _extract_product_data(self, product_description):
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

        brand = self.find_exactly_one_element(brands, product_description)
        if not brand:
            logger.warning(f'Brand not found in product [{product_description}]')
            return None, None

        lineup_type_result = self.find_exactly_one_element(lineup_type, product_description)
        product_class = self.find_exactly_one_element(product_classes, product_description)

        product_type = None
        if lineup_type_result and product_class in higher_lineup[
            lineup_type_result] or product_class in standard_lineup:
            product_type = product_class

        if product_type is not None and lineup_type_result is not None:
            product_type += f' {lineup_type_result}'

        return brand, product_type


if __name__ == '__main__':
    fetcher = NVidiaFetcher()
    fetcher.continuous_watch()
