# coding: utf-8

from vendor import Vendor


class Cybertek(Vendor):
    def __init__(self):
        sites = [
            'http://bit.do/eL5BS',  # GTX 1060 6GB
            'http://bit.do/eL5B9',  # GTX 1660
            'http://bit.do/eL5Cr',  # GTX 1660 Ti
            'http://bit.do/eL5Cz',  # RTX 2060
            'http://bit.do/eL5CG',  # RTX 2070
            'http://bit.do/eL5CQ',  # RTX 2080
            'http://bit.do/eL5CU',  # RTX 2080 Ti
        ]
        super().__init__(source_name=__class__.__name__, sites=sites)

    def enrich_deals_from_soup(self, soup, deals):
        products = soup.find('div', attrs={'class': 'categorie-filtre lst_grid'})
        for item in products.findAll('div'):
            try:
                fiche = item.find('a', attrs={'title': 'Voir la fiche produit'})
                for element_to_remove in ['prodfiche_destoc', 'prodfiche_dispo', 'prodfiche_nodispo',
                                          'prodfiche_mag']:
                    try:
                        fiche.find('span', attrs={'class': element_to_remove}).decompose()
                    except:
                        pass
                product_name = fiche.text
                product_price = self.clean_price(item.find('div', attrs={'class': 'price_prod_resp'}).text)
                deals[product_name] = product_price
            except:
                pass
