import re
import urllib.request
import bs4 as BeautifulSoup


def clean_price(dirty_price):
    m = re.search('([0-9.,]+)', dirty_price)
    return m.group(0)


class TopAchat:
    def __init__(self):
        self.source_name = __class__.__name__
    
    @staticmethod
    def fetch_deals():
        deals = {}
        with urllib.request.urlopen('https://bit.ly/2NpfsSV') as response:
            html = response.read()
            soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
            for item in soup.findAll('article', attrs={'class': 'grille-produit'}):
                product_name = item.find('h3').text
                product_price = clean_price(item.find('div', attrs={'itemprop': 'price'}).text)
                deals[product_name] = product_price
        return deals


if __name__ == '__main__':
    clean_price('      422.45   €*')
    clean_price('   ---   422,45   €*')
