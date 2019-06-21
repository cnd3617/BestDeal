# coding: utf-8

import sqlite3
from loguru import logger
from datetime import datetime, timezone


def dict_factory(cursor, row):
    """
    Useful to generate dict from queries (instead of tuples)
    """
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
    def __init__(self, filename='PricesHistorization.db'):
        logger.info('Connecting to database [{}]'.format(filename))
        # isolation_level=None => auto commit
        self.connection = sqlite3.connect(database=filename, isolation_level=None)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        queries = [
            'CREATE TABLE IF NOT EXISTS product '
            '(product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, product_type TEXT)',

            'CREATE TABLE IF NOT EXISTS source '
            '(source_id INTEGER PRIMARY KEY AUTOINCREMENT, source_name TEXT UNIQUE)',

            'CREATE TABLE IF NOT EXISTS histo '
            '(histo_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'histo_price REAL,'
            'histo_date TEXT, '
            'product_id INTEGER NOT NULL REFERENCES product(product_id), '
            'source_id INTEGER NOT NULL REFERENCES source(source_id))'
        ]
        for query in queries:
            self.cursor.execute(query)
        self.connection.commit()

    @staticmethod
    def get_today_date():
        return datetime.now(timezone.utc).strftime('%Y%m%d')

    @staticmethod
    def get_today_datetime():
        return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')

    def generic_insert(self, table, columns, values):
        query = 'INSERT INTO {} ({}) VALUES({})'.format(table, ','.join(columns), ','.join(['?']*len(values)))
        logger.trace('Query [{}]'.format(query))
        self.cursor.execute(query, tuple(values,))
        return self.cursor.lastrowid

    def generic_select(self, table, columns, where_clause, additional_clause=''):
        selected_columns = ','.join(columns) if columns else '*'
        query = 'SELECT {} FROM {} where {} {}'.format(selected_columns, table, where_clause, additional_clause)
        logger.trace('Query [{}]'.format(query))
        self.cursor.execute(query)
        fetched_values = self.cursor.fetchall()
        logger.trace('Fetched values [{}]'.format(fetched_values))
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
            logger.info('New [{}]: {}'.format(table, values))
            object_id = self.generic_insert(table, columns, values)
        return object_id

    def add_price(self, product_id, source_id, histo_price, histo_date):
        return self.generic_insert(table='histo',
                                   columns=['product_id', 'source_id', 'histo_price', 'histo_date'],
                                   values=[product_id, source_id, histo_price, histo_date])

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
                                             additional_clause=' AND histo.histo_date like "{}_%" ORDER BY histo_date DESC LIMIT 1'.format(self.get_today_date()))
        if fetched_values:
            assert (len(fetched_values) == 1)
            return float(fetched_values[0]['histo_price'])
        return None

    def get_cheapest_price(self, source_id, product_type, histo_date):
        """
        DEPRECATED
        TODO: REMOVE THIS
        """
        query = 'SELECT MIN(histo.histo_price) AS histo_price, histo.histo_date, product.product_name ' \
                'FROM histo, product ' \
                'WHERE histo.source_id = "{}" AND ' \
                'product.product_id = histo.product_id AND ' \
                'product.product_type = "{}" AND ' \
                'histo.histo_date like "{}_%"'.format(source_id, product_type, histo_date)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_source_identifiers(self):
        """
        SELECT source_id, source_name
        FROM source
        """
        query = 'SELECT source_id, source_name FROM source'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_prices(self):
        query = 'SELECT * ' \
                'FROM histo ' \
                'ORDER BY histo.histo_date'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_products(self):
        query = 'SELECT * ' \
                'FROM product '
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_product_types(self):
        query = 'SELECT distinct(product_type) ' \
                'FROM product ' \
                'ORDER BY product_type'
        self.cursor.execute(query)
        return [x['product_type'] for x in self.cursor.fetchall()]

    def get_cheapest(self, product_type, histo_date):
        query = 'SELECT product_name, product_type, histo_price, source_name ' \
                'FROM histo, product, source ' \
                'WHERE source.source_id = histo.source_id ' \
                'AND product.product_id = histo.product_id ' \
                'AND histo.histo_date LIKE "{}_%" ' \
                'AND product.product_type = "{}"'.format(histo_date, product_type)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        cheapest = None
        for row in rows:
            if cheapest is None or float(row['histo_price']) < float(cheapest['histo_price']):
                cheapest = row
        return cheapest

    def get_cheapest_from_specific_source(self, product_type, histo_date, source_id):
        query = 'SELECT product_name, histo_price, source_name ' \
                'FROM histo, product, source ' \
                'WHERE source.source_id = histo.source_id ' \
                'AND source.source_id = {} ' \
                'AND product.product_id = histo.product_id ' \
                'AND histo.histo_date LIKE "{}_%" ' \
                'AND product.product_type = "{}"'.format(source_id, histo_date, product_type)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        cheapest = None
        for row in rows:
            if cheapest is None or float(row['histo_price']) < float(cheapest['histo_price']):
                cheapest = row
        return cheapest


if __name__ == '__main__':
    db = PriceDatabase()
    # logger.info(db.get_cheapest('2080', '20190621'))
    # logger.info(db.get_cheapest('1060', '20190101', 1))
