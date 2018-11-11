import re
import urllib.request
import bs4 as BeautifulSoup
import requests


def clean_price(dirty_price):
    """
    Clean the price to facilitate comparisons
    """
    m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
    return '{}.{}'.format(m.group(1), m.group(2))


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}


class RueDuCommerce:
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        sites = [
            'https://bit.ly/2ApT5JK',  # GTX 1080 Ti
            'https://bit.ly/2OMZJ5E',  # RTX 2080
            'https://bit.ly/2CCjB4b',  # RTX 2080 Ti
        ]
        deals = {}
        for site in sites:
            html = requests.get(url=site, headers=headers)
            soup = BeautifulSoup.BeautifulSoup(html.text, 'html.parser')
            for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
                product_name = item.find('div', attrs={'class': 'summary'}).text
                product_price = clean_price(item.find('div', attrs={'class': 'price'}).text)
                deals[product_name] = product_price
        return deals


class GrosBill:
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        site = 'https://bit.ly/2yEd9WQ'
        html = requests.get(url=site, headers=headers)
        soup = BeautifulSoup.BeautifulSoup(html.text, 'html.parser')
        deals = {}
        for product in soup.find('table', attrs={'id': 'listing_mode_display'}).findAll('tr'):
            try:
                product_name = product.find('div', attrs={'class': 'product_description'}).find('a').text
                product_price = clean_price(product.find('td', attrs={'class': 'btn_price_wrapper'}).find('b').text)
                deals[product_name] = product_price
            except Exception as exception:
                print(exception)
        return deals


class CDiscount:
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        sites = [
            'https://bit.ly/2O2raU4',  # GTX 1080 Ti
            'https://bit.ly/2Pi0W4r',  # RTX 2080
            'https://bit.ly/2yzGzWO',  # RTX 2080 Ti
        ]
        deals = {}
        for site in sites:
            html = requests.get(url=site, headers=headers)
            soup = BeautifulSoup.BeautifulSoup(html.text, 'html.parser')
            for item in soup.findAll('div', attrs={'class': 'jsPrdBlocContainer'}):
                product_name = item.find('div', attrs={'class': 'prdtBILTit'}).text
                filtered_words = ['Aquacomputer', 'Watercooling', 'Alphacool', 'Acrylic', 'Ventilation', 'igame']
                if any(word in product_name for word in filtered_words):
                    continue
                product_price = clean_price(item.find('span', attrs={'class': 'price'}).text)
                deals[product_name] = product_price
        return deals


class TopAchat:
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        deals = {}
        with urllib.request.urlopen('https://bit.ly/2yejyJ4') as response:
            html = response.read()
            soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
            for item in soup.findAll('article', attrs={'class': 'grille-produit'}):
                product_name = item.find('h3').text
                product_price = clean_price(item.find('div', attrs={'itemprop': 'price'}).text)
                deals[product_name] = product_price
        return deals


class HardwareShop:
    """
    TODO: FIX ME
    """
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        site = 'https://bit.ly/2PhtQBO'
        html = requests.get(url=site, headers=headers)
        soup = BeautifulSoup.BeautifulSoup(html.text, 'html.parser')
        print(soup.prettify())
        deals = {}
        items = soup.find_all('li', attrs={'data-ref': re.compile("[A-Za-z0-9]")})
        for item in items:
            product_name = item.find('div', attrs={'class': 'description'}).find('h2').text
            for script_section in soup.findAll('script'):
                if '.price-wrapper' in script_section.text:
                    print(script_section.prettify())

            product_price = clean_price(item.find('div', attrs={'class': 'price_prod_resp'}).text)
            deals[product_name] = product_price
        return deals


class Cybertek:
    """
    TODO: improve this scrapper
    """
    def __init__(self):
        self.source_name = __class__.__name__

    @staticmethod
    def fetch_deals():
        site = 'https://bit.ly/2PJsdtN'
        html = requests.get(url=site, headers=headers)
        soup = BeautifulSoup.BeautifulSoup(html.text, 'html.parser')
        deals = {}
        products = soup.find('div', attrs={'class': 'categorie-filtre lst_grid'})
        for item in products.findAll('div'):
            try:
                fiche = item.find('a', attrs={'title': 'Voir la fiche produit'})
                for element_to_remove in ['prodfiche_destoc', 'prodfiche_dispo', 'prodfiche_nodispo', 'prodfiche_mag']:
                    try:
                        fiche.find('span', attrs={'class': element_to_remove}).decompose()
                    except:
                        pass
                product_name = fiche.text
                product_price = clean_price(item.find('div', attrs={'class': 'price_prod_resp'}).text)
                deals[product_name] = product_price
            except:
                pass
        return deals


if __name__ == '__main__':
    for deal in Cybertek.fetch_deals():
        print(deal)
    # for case in ['      422.45   €*', '   ---   422,45   €*', '422€45']:
    #     print('[%s] -> [%s]' % (case, clean_price(case)))
