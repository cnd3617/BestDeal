import re
import urllib.request
import bs4 as BeautifulSoup


def clean_price(dirty_price):
    """
    Clean the price to facilitate comparisons
    """
    m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
    return '{}.{}'.format(m.group(1), m.group(2))


class CDiscount:
    def __init__(self):
        self.source_name = __class__.__name__
        
    @staticmethod
    def fetch_deals():
        deals = {}
        with urllib.request.urlopen('https://bit.ly/2A5clfN') as response:
            html = response.read()
            soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
            # print(soup.prettify())
            for item in soup.findAll('div', attrs={'class': 'jsPrdBlocContainer'}):
                product_name = item.find('div', attrs={'class': 'prdtBILTit'}).text
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


if __name__ == '__main__':
    for case in ['      422.45   €*', '   ---   422,45   €*', '422€45']:
        print('[%s] -> [%s]' % (case, clean_price(case)))
