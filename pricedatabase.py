import logging
import sqlite3
from datetime import datetime, timezone


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class PriceDatabase:
    """
    PRODUCT: product_id, product_name, product_type
    SOURCE = source_id, source_name
    HISTO = histo_id, product_id, source_id, histo_price, histo_date
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.today_date = datetime.now(timezone.utc).strftime('%Y%m%d')
        self.today_datetime = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        # isolation_level=None => auto commit
        self.connection = sqlite3.connect(database='PricesHistorization.db', isolation_level=None)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        queries = [
            'CREATE TABLE IF NOT EXISTS product '
            '(product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, product_type TEXT)',

            'CREATE TABLE IF NOT EXISTS source '
            '(source_id INTEGER PRIMARY KEY AUTOINCREMENT, source_name TEXT UNIQUE)',

            'CREATE TABLE IF NOT EXISTS histo '
            '(histo_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'histo_price TEXT, histo_date TEXT, '
            'product_id INTEGER NOT NULL REFERENCES product(product_id), '
            'source_id INTEGER NOT NULL REFERENCES source(source_id))'
        ]
        for query in queries:
            self.cursor.execute(query)
        self.connection.commit()
        
    def generic_insert(self, table, columns, values):
        query = 'INSERT INTO {} ({}) VALUES({})'.format(table, ','.join(columns), ','.join(['?']*len(values)))
        self.logger.debug('Query [{}]'.format(query))
        self.cursor.execute(query, tuple(values,))
        return self.cursor.lastrowid

    def generic_select(self, table, columns, where_clause, additional_clause=''):
        selected_columns = ','.join(columns) if columns else '*'
        query = 'SELECT {} FROM {} where {} {}'.format(selected_columns, table, where_clause, additional_clause)
        self.logger.debug('Query [{}]'.format(query))
        self.cursor.execute(query)
        fetched_values = self.cursor.fetchall()
        self.logger.debug('Fetched values [{}]'.format(fetched_values))
        return fetched_values
    
    def get_object_id(self, table, columns, where_clause):
        fetched_values = self.generic_select(table, columns, where_clause)
        # fetched_values should be a list containing 1 dict
        if fetched_values:
            for key in fetched_values[0].keys():
                if 'id' in key:
                    return fetched_values[0][key]
        return None
    
    def insert_if_necessary(self, table, columns, values):
        where_clause = self.build_where_clause(columns, values)
        object_id = self.get_object_id(table, ['{}_id'.format(table)], where_clause)
        if object_id is None:
            self.logger.info('New [{}]: {}'.format(table, values))
            object_id = self.generic_insert(table, columns, values)
        return object_id
    
    def add_price(self, product_id, source_id, histo_price):
        return self.generic_insert(table='histo',
                                   columns=['product_id', 'source_id', 'histo_price', 'histo_date'],
                                   values=[product_id, source_id, histo_price, self.today_datetime])
    
    @staticmethod
    def build_where_clause(columns, values):
        enclosed_values = ['"{}"'.format(value) for value in values]
        where_clause = ' and '.join(['='.join(t) for t in zip(columns, enclosed_values)])
        return where_clause
    
    def get_last_price_for_today(self, product_id, source_id):
        """
        SELECT histo_price, histo_date FROM histo WHERE product_id=45 AND source_id=2 AND histo.histo_date like '20181013_%' ORDER BY histo_date DESC LIMIT 1
        """
        where_clause = self.build_where_clause(columns=['product_id', 'source_id'], values=[product_id, source_id])
        fetched_values = self.generic_select(table='histo',
                                             columns=['histo_price'],
                                             where_clause=where_clause,
                                             additional_clause=' AND histo.histo_date like "{}_%" ORDER BY histo_date DESC LIMIT 1'.format(self.today_date))
        if fetched_values:
            assert (len(fetched_values) == 1)
            return fetched_values[0]['histo_price']
        return None
    
    def get_cheapest_price(self, product_id, source_id):
        """
        SELECT min(histo_price), histo_date FROM histo WHERE product_id=1 AND source_id=1
        """
        where_clause = self.build_where_clause(columns=['product_id', 'source_id'], values=[product_id, source_id])
        fetched_values = self.generic_select(table='histo', columns=['min(histo_price)'], where_clause=where_clause)
        if fetched_values:
            return fetched_values[0]['min(histo_price)']
        return None

    def get_cheapest_by_product_type(self):
        query = 'SELECT product_name, product_type, min(histo_price) AS histo_price, histo_date, source_name ' \
                'FROM histo, product, source ' \
                'WHERE product.product_id = histo.product_id AND histo.histo_date like "20181014_%" ' \
                'GROUP BY product_type'
        self.cursor.execute(query)
        return self.cursor.fetchall()
