import sys
import pricedatabase
import logging
import dealscrappers


class BestDeal:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = pricedatabase.PriceDatabase()

    @staticmethod
    def extract_product_type(product_name):
        product_type = None
        for model in ['1070', '1080', '2060', '2070', '2080']:
            if model in product_name:
                product_type = 'GTX ' + model
        if product_type and (' ti' in product_name.lower() or 'ti ' in product_name.lower()):
            product_type += ' Ti'
        return product_type

    def display_best_deals(self):
        cheapest_products = self.db.get_cheapest_by_product_type()
        self.logger.info('Best deals for [{}]'.format(self.db.today_date))
        for product in cheapest_products:
            self.logger.info('Cheapest [{product_type}] [{source_name}] -> [{product_name}] for [{histo_price}]€'.format(**product))

    def record_best_deals(self):
        sources = [dealscrappers.TopAchat, dealscrappers.CDiscount]
        for source in sources:
            self.logger.info('Fetch deals from [{}]'.format(source.__name__))
            deals = source.fetch_deals()
            for product_name, product_price in deals.items():
                product_type = self.extract_product_type(product_name)
                if product_type:
                    self.update_price(product_name, product_type, source.__name__, product_price)
                else:
                    self.logger.debug('Ignoring [{}]'.format(product_name))

    def update_price(self, product_name, product_type, source_name, new_price):
        source_id = self.db.insert_if_necessary(table='source',  columns=['source_name'], values=[source_name])
        product_id = self.db.insert_if_necessary(table='product', columns=['product_name', 'product_type'], values=[product_name, product_type])
        today_last_price = self.db.get_last_price_for_today(product_id, source_id)
        if today_last_price is None or today_last_price != new_price:
            previous_price_info = 'Today last price [{}]'.format(today_last_price) if today_last_price else ''
            self.logger.info('New price for [{}] from [{}] : [{}] {}'.format(product_name, source_name, new_price, previous_price_info))
            self.db.add_price(product_id, source_id, new_price)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S %p')
    bd = BestDeal()
    bd.record_best_deals()
    bd.display_best_deals()
